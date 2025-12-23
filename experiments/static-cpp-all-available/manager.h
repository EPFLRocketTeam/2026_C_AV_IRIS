
#include <iostream>
#include <cstdint>

struct CallRecord {
    const char* message;
    const char* file;
    int line;
};

extern const CallRecord __start_calls;
extern const CallRecord __stop_calls;

#define _InternalStringToIndex(data) ([]{ \
        static const char msg[] = data; \
        static const CallRecord record \
        __attribute__((section("calls"), used, aligned(1))) \
        = { msg, __FILE__, __LINE__ }; \
        return (int) ((&record) - (&__start_calls)); \
    })()

#define StringToIndex(data) ([] { \
        static uint64_t val = _InternalStringToIndex(data); \
        std::cout << "String \"" data << "\" has index " << val << std::endl; \
        return val; \
    })();
