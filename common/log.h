#pragma once

#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>

namespace oniku {

class FailMessageStream {
public:
    FailMessageStream(const std::string msg, const char* func, const char* file, int line)
        : msg_(msg), func_(func), file_(file), line_(line) {}

    ~FailMessageStream() {
        std::cerr << msg_ << " in " << func_ << " at " << file_ << ":" << line_ << ": " << oss_.str() << std::endl;
        std::abort();
    }

    template <class T>
    FailMessageStream& operator<<(const T& v) {
        oss_ << v;
        return *this;
    }

private:
    std::ostringstream oss_;
    const std::string msg_;
    const char* func_;
    const char* file_;
    const int line_;
};

#define CHECK(cond) \
    while (!(cond)) oniku::FailMessageStream("Check `" #cond "' failed!", __func__, __FILE__, __LINE__)

#define CHECK_CMP(a, b, op) \
    while (!((a)op(b)))     \
    oniku::FailMessageStream("Check `" #a "' " #op " `" #b "' failed!", __func__, __FILE__, __LINE__) << "(" << a << " vs " << b << ")"

#define CHECK_EQ(a, b) CHECK_CMP(a, b, ==)
#define CHECK_NE(a, b) CHECK_CMP(a, b, !=)
#define CHECK_LT(a, b) CHECK_CMP(a, b, <)
#define CHECK_LE(a, b) CHECK_CMP(a, b, <=)
#define CHECK_GT(a, b) CHECK_CMP(a, b, >)
#define CHECK_GE(a, b) CHECK_CMP(a, b, >=)

#ifdef NDEBUG
#define DCHECK(cond)
#define DCHECK_EQ(a, b)
#define DCHECK_NE(a, b)
#define DCHECK_LT(a, b)
#define DCHECK_LE(a, b)
#define DCHECK_GT(a, b)
#define DCHECK_GE(a, b)
#else
#define DCHECK(cond) CHECK(cond)
#define DCHECK_EQ(a, b) CHECK_EQ(a, b)
#define DCHECK_NE(a, b) CHECK_NE(a, b)
#define DCHECK_LT(a, b) CHECK_LT(a, b)
#define DCHECK_LE(a, b) CHECK_LE(a, b)
#define DCHECK_GT(a, b) CHECK_GT(a, b)
#define DCHECK_GE(a, b) CHECK_GE(a, b)
#endif

}  // namespace oniku
