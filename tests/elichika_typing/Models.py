import numpy as np
import pprint
import unittest

from chainer_compiler.elichika.testtools import generate_id2type_from_forward

from testcases.elichika_tests.model.MLP import MLP
from testcases.elichika_tests.model.Resnet_with_loss import ResNet50


class TestMLP(unittest.TestCase):
    def test_MLP(self):
        out_n = 4
        batch_size = 100
        model = MLP(8, out_n)
        v = np.random.rand(batch_size, 3).astype(np.float32)
        w = np.random.randint(out_n, size=batch_size)

        id2type = generate_id2type_from_forward(model, (v, w))

        self.assertEqual(str(id2type[1]), "MLP -> ndarray(dtype(float32)) -> ndarray(dtype(int64)) -> Variable(dtype(float32))")	# FunctionDef (line 1)
        self.assertEqual(str(id2type[9]), "NoneType")	# Assign (line 2)
        self.assertEqual(str(id2type[10]), "Variable(dtype(float32))")	# Name (line 2)
        self.assertEqual(str(id2type[12]), "Variable(dtype(float32))")	# Call (line 2)
        self.assertEqual(str(id2type[13]), "Variable(dtype(float32)) -> Variable(dtype(float32))")	# Attribute (line 2)
        self.assertEqual(str(id2type[17]), "Variable(dtype(float32))")	# Call (line 2)
        self.assertEqual(str(id2type[18]), "Variable(dtype(float32)) -> Variable(dtype(float32))")	# Attribute (line 2)
        self.assertEqual(str(id2type[22]), "ndarray(dtype(float32))")	# Name (line 2)
        self.assertEqual(str(id2type[24]), "NoneType")	# Assign (line 3)
        self.assertEqual(str(id2type[25]), "Variable(dtype(float32))")	# Name (line 3)
        self.assertEqual(str(id2type[27]), "Variable(dtype(float32))")	# Call (line 3)
        self.assertEqual(str(id2type[28]), "Variable(dtype(float32)) -> Variable(dtype(float32))")	# Attribute (line 3)
        self.assertEqual(str(id2type[32]), "Variable(dtype(float32))")	# Call (line 3)
        self.assertEqual(str(id2type[33]), "Variable(dtype(float32)) -> Variable(dtype(float32))")	# Attribute (line 3)
        self.assertEqual(str(id2type[37]), "Variable(dtype(float32))")	# Name (line 3)
        self.assertEqual(str(id2type[39]), "NoneType")	# Assign (line 4)
        self.assertEqual(str(id2type[40]), "Variable(dtype(float32))")	# Name (line 4)
        self.assertEqual(str(id2type[42]), "Variable(dtype(float32))")	# Call (line 4)
        self.assertEqual(str(id2type[43]), "Variable(dtype(float32)) -> Variable(dtype(float32))")	# Attribute (line 4)
        self.assertEqual(str(id2type[47]), "Variable(dtype(float32))")	# Name (line 4)
        self.assertEqual(str(id2type[49]), "NoneType")	# Assign (line 5)
        self.assertEqual(str(id2type[50]), "Variable(dtype(float32))")	# Name (line 5)
        self.assertEqual(str(id2type[52]), "Variable(dtype(float32))")	# Call (line 5)
        self.assertEqual(str(id2type[53]), "Variable(dtype(float32)) -> ndarray(dtype(int64)) -> Variable(dtype(float32))")	# Attribute (line 5)
        self.assertEqual(str(id2type[57]), "Variable(dtype(float32))")	# Name (line 5)
        self.assertEqual(str(id2type[59]), "ndarray(dtype(int64))")	# Name (line 5)
        self.assertEqual(str(id2type[61]), "Variable(dtype(float32))")	# Return (line 6)
        self.assertEqual(str(id2type[62]), "Variable(dtype(float32))")	# Name (line 6)



class TestResNet50(unittest.TestCase):
    def test_ResNet50(self):
        model = ResNet50()
        bsize = 2
        v = np.random.rand(bsize, 3, 224, 224).astype(np.float32)
        t = np.random.randint(1000, size=bsize).astype(np.int32)

        id2type = generate_id2type_from_forward(model, (v, t))


        self.assertEqual(str(id2type[1]), "ResNet50 -> ndarray(dtype(float32)) -> ndarray(dtype(int32)) -> Variable(dtype(float32))")	# FunctionDef forward (line 1)
        self.assertEqual(str(id2type[9]), "NoneType")	# Assign (line 2)
        self.assertEqual(str(id2type[10]), "Variable(dtype(float32))")	# Name h (line 2)
        self.assertEqual(str(id2type[12]), "Variable(dtype(float32))")	# Call (line 2)
        self.assertEqual(str(id2type[13]), "Variable(dtype(float32)) -> Variable(dtype(float32))")	# Attribute bn1 (line 2)
        self.assertEqual(str(id2type[14]), "ResNet50")	# Name self (line 2)
        self.assertEqual(str(id2type[17]), "Variable(dtype(float32))")	# Call (line 2)
        self.assertEqual(str(id2type[18]), "Variable(dtype(float32)) -> Variable(dtype(float32))")	# Attribute conv1 (line 2)
        self.assertEqual(str(id2type[19]), "ResNet50")	# Name self (line 2)
        self.assertEqual(str(id2type[22]), "ndarray(dtype(float32))")	# Name x (line 2)
        self.assertEqual(str(id2type[24]), "NoneType")	# Assign (line 3)
        self.assertEqual(str(id2type[25]), "Variable(dtype(float32))")	# Name h (line 3)
        self.assertEqual(str(id2type[27]), "Variable(dtype(float32))")	# Call (line 3)
        self.assertEqual(str(id2type[28]), "Variable(dtype(float32)) -> int -> Variable(dtype(float32))")	# Attribute max_pooling_2d (line 3)
        self.assertEqual(str(id2type[32]), "Variable(dtype(float32))")	# Call (line 3)
        self.assertEqual(str(id2type[33]), "Variable(dtype(float32)) -> Variable(dtype(float32))")	# Attribute relu (line 3)
        self.assertEqual(str(id2type[37]), "Variable(dtype(float32))")	# Name h (line 3)
        self.assertEqual(str(id2type[39]), "int")	# Num (line 3)
        self.assertEqual(str(id2type[42]), "NoneType")	# Assign (line 4)
        self.assertEqual(str(id2type[43]), "Variable(dtype(float32))")	# Name h (line 4)
        self.assertEqual(str(id2type[45]), "Variable(dtype(float32))")	# Call (line 4)
        self.assertEqual(str(id2type[46]), "Variable(dtype(float32)) -> Variable(dtype(float32))")	# Attribute res2 (line 4)
        self.assertEqual(str(id2type[47]), "ResNet50")	# Name self (line 4)
        self.assertEqual(str(id2type[50]), "Variable(dtype(float32))")	# Name h (line 4)
        self.assertEqual(str(id2type[52]), "NoneType")	# Assign (line 5)
        self.assertEqual(str(id2type[53]), "Variable(dtype(float32))")	# Name h (line 5)
        self.assertEqual(str(id2type[55]), "Variable(dtype(float32))")	# Call (line 5)
        self.assertEqual(str(id2type[56]), "Variable(dtype(float32)) -> Variable(dtype(float32))")	# Attribute res3 (line 5)
        self.assertEqual(str(id2type[57]), "ResNet50")	# Name self (line 5)
        self.assertEqual(str(id2type[60]), "Variable(dtype(float32))")	# Name h (line 5)
        self.assertEqual(str(id2type[62]), "NoneType")	# Assign (line 6)
        self.assertEqual(str(id2type[63]), "Variable(dtype(float32))")	# Name h (line 6)
        self.assertEqual(str(id2type[65]), "Variable(dtype(float32))")	# Call (line 6)
        self.assertEqual(str(id2type[66]), "Variable(dtype(float32)) -> Variable(dtype(float32))")	# Attribute res4 (line 6)
        self.assertEqual(str(id2type[67]), "ResNet50")	# Name self (line 6)
        self.assertEqual(str(id2type[70]), "Variable(dtype(float32))")	# Name h (line 6)
        self.assertEqual(str(id2type[72]), "NoneType")	# Assign (line 7)
        self.assertEqual(str(id2type[73]), "Variable(dtype(float32))")	# Name h (line 7)
        self.assertEqual(str(id2type[75]), "Variable(dtype(float32))")	# Call (line 7)
        self.assertEqual(str(id2type[76]), "Variable(dtype(float32)) -> Variable(dtype(float32))")	# Attribute res5 (line 7)
        self.assertEqual(str(id2type[77]), "ResNet50")	# Name self (line 7)
        self.assertEqual(str(id2type[80]), "Variable(dtype(float32))")	# Name h (line 7)
        self.assertEqual(str(id2type[82]), "NoneType")	# Assign (line 8)
        self.assertEqual(str(id2type[83]), "Variable(dtype(float32))")	# Name h (line 8)
        self.assertEqual(str(id2type[85]), "Variable(dtype(float32))")	# Call (line 8)
        self.assertEqual(str(id2type[86]), "Variable(dtype(float32)) -> int -> Variable(dtype(float32))")	# Attribute average_pooling_2d (line 8)
        self.assertEqual(str(id2type[90]), "Variable(dtype(float32))")	# Name h (line 8)
        self.assertEqual(str(id2type[92]), "int")	# Num (line 8)
        self.assertEqual(str(id2type[95]), "NoneType")	# Assign (line 9)
        self.assertEqual(str(id2type[96]), "Variable(dtype(float32))")	# Name h (line 9)
        self.assertEqual(str(id2type[98]), "Variable(dtype(float32))")	# Call (line 9)
        self.assertEqual(str(id2type[99]), "Variable(dtype(float32)) -> Variable(dtype(float32))")	# Attribute fc (line 9)
        self.assertEqual(str(id2type[100]), "ResNet50")	# Name self (line 9)
        self.assertEqual(str(id2type[103]), "Variable(dtype(float32))")	# Name h (line 9)
        self.assertEqual(str(id2type[105]), "NoneType")	# Assign (line 11)
        self.assertEqual(str(id2type[106]), "Variable(dtype(float32))")	# Name loss (line 11)
        self.assertEqual(str(id2type[108]), "Variable(dtype(float32))")	# Call (line 11)
        self.assertEqual(str(id2type[109]), "Variable(dtype(float32)) -> ndarray(dtype(int32)) -> Variable(dtype(float32))")	# Attribute softmax_cross_entropy (line 11)
        self.assertEqual(str(id2type[113]), "Variable(dtype(float32))")	# Name h (line 11)
        self.assertEqual(str(id2type[115]), "ndarray(dtype(int32))")	# Name t (line 11)
        self.assertEqual(str(id2type[117]), "Variable(dtype(float32))")	# Return (line 13)
        self.assertEqual(str(id2type[118]), "Variable(dtype(float32))")	# Name loss (line 13)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
