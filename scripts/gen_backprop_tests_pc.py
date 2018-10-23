#!/usr/bin/python3

import os
import sys

import chainer
import numpy as np
import onnx
from onnx import onnx_pb

my_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(my_path))
sys.path.append(os.path.join(my_path, 'ch2o'))
import ch2o
from oniku.scripts import onnx_chainer_util

F = chainer.functions
L = chainer.links


def create_backprop_test(test_name, model, input_values):
    chainer.config.train = True
    model.cleargrads()
    output_values = model(*map(chainer.variable.Variable, input_values))

    test_dir = 'out/backprop_test_pc_%s' % test_name
    test_data_set_dir = os.path.join(test_dir, 'test_data_set_0')
    onnx_chainer_util.makedirs(test_data_set_dir)

    xmodel = ch2o.compile_model(model, input_values)
    all_input_tensors = xmodel.graph.input
    output_tensors = xmodel.graph.output

    if not isinstance(output_values, (list, tuple)):
        output_values = (output_values,)
    for output_value in output_values:
        output_value.grad = np.ones(output_value.shape, output_value.dtype)
        output_value.backward()

    ch2o.testcasegen.edit_onnx_protobuf(xmodel, model)

    with open(os.path.join(test_dir, 'model.onnx'), 'wb') as fp:
        fp.write(xmodel.SerializeToString())

    initializer_names = set()
    for initializer in xmodel.graph.initializer:
        initializer_names.add(initializer.name)
    input_tensors = []
    for input_tensor in all_input_tensors:
        if input_tensor.name not in initializer_names:
            input_tensors.append(input_tensor)

    assert len(input_tensors) == len(input_values)
    assert len(output_tensors) == len(output_values)

    outputs = []
    for tensor, value in zip(output_tensors, output_values):
        outputs.append((tensor, value.array))
    for name, param in sorted(model.namedparams()):
        bp_name = onnx.helper.make_tensor_value_info(
            'grad_out@' + name, onnx.TensorProto.FLOAT, ())
        outputs.append((bp_name, param.grad))

    ch2o.testcasegen.dump_test_inputs_outputs(
        list(zip(input_tensors, input_values)),
        outputs,
        test_data_set_dir)


class BackpropTest(object):
    def __init__(self, name, model, inputs, rtol=1e-4, fail=False):
        self.name = name
        self.model = model
        self.inputs = inputs
        self.rtol = rtol
        self.fail = fail

    def generate(self):
        create_backprop_test(self.name, self.model, self.inputs)


def get_backprop_tests():
    F = chainer.functions
    tests = []

    def test(name, model, *inputs, rtol=1e-4, fail=False):
        tests.append(BackpropTest(name, model, inputs, rtol=rtol, fail=fail))

    def aranges(*shape):
        r = 1
        for d in shape:
            r *= d
        return np.arange(r).reshape(shape).astype(np.float32)

    class Nop(chainer.Chain):
        def forward(self, x):
            return x

    test('nop', Nop(), aranges(2, 3))

    class AddSelf(chainer.Chain):
        def forward(self, x):
            return x + x

    test('add_self', AddSelf(), aranges(2, 3))

    class Linear(chainer.Chain):
        def __init__(self):
            super(Linear, self).__init__()
            with self.init_scope():
                self.l1 = L.Linear(None, 10)

        def forward(self, x):
            return F.relu(self.l1(x))

    test('linear', Linear(), aranges(2, 3))

    class SoftmaxCrossEntropy(chainer.Chain):
        def __init__(self):
            super(SoftmaxCrossEntropy, self).__init__()
            with self.init_scope():
                self.l1 = L.Linear(None, 10)

        def forward(self, x, t):
            return F.softmax_cross_entropy(self.l1(x), t)

    test('softmax_cross_entropy', SoftmaxCrossEntropy(),
         aranges(2, 3), np.array([1, 0]))

    class LRN(chainer.Chain):
        def __init__(self):
            super(LRN, self).__init__()
            with self.init_scope():
                self.l1 = L.Linear(None, 10)

        def forward(self, x):
            return F.local_response_normalization(self.l1(x))

    test('lrn', LRN(), aranges(2, 3))

    class Stack(chainer.Chain):
        def __init__(self, axis):
            super(Stack, self).__init__()
            self.axis = axis
            with self.init_scope():
                self.l1 = L.Linear(None, 4)
                self.l2 = L.Linear(None, 4)

        def forward(self, x, y):
            xs = [self.l1(x) * 2, self.l2(y) * 3]
            return F.stack(xs, axis=self.axis)

    test('stack', Stack(0), aranges(2, 3), aranges(2, 3) + 1)
    test('stack_axis1', Stack(1), aranges(2, 3), aranges(2, 3) + 1)

    class Concat(chainer.Chain):
        def __init__(self, axis):
            super(Concat, self).__init__()
            self.axis = axis
            with self.init_scope():
                self.l1 = L.Linear(None, 4)
                self.l2 = L.Linear(None, 4)

        def forward(self, x, y):
            xs = [self.l1(x) * 2, self.l2(y) * 3]
            return F.concat(xs, axis=self.axis)

    test('concat', Concat(0), aranges(2, 3), aranges(2, 3) + 1)
    test('concat_axis1', Concat(1), aranges(2, 3), aranges(2, 3) + 1)

    class Lookup(chainer.Chain):
        def __init__(self):
            super(Lookup, self).__init__()
            with self.init_scope():
                self.l1 = L.Linear(None, 4)
                self.l2 = L.Linear(None, 4)

        def forward(self, x, y, z):
            xs = [self.l1(x) * 2, self.l1(y) * 3, self.l2(z) * 4]
            return xs[0] * xs[2] * xs[0] * xs[1] * xs[2] * xs[2]

    test('lookup', Lookup(),
         aranges(2, 3), aranges(2, 3) + 1, aranges(2, 3) + 2)

    return tests


def main():
    for test in get_backprop_tests():
        np.random.seed(42)
        test.generate()


if __name__ == '__main__':
    sys.argv.append('--quiet')
    sys.argv.append('/tmp/dummy_dir')
    main()
