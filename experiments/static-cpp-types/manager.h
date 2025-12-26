
#include <stddef.h>

struct TypeRecord {
    void (*registerFunction) ();
};

template<typename T>
int get_type_id ();
template<typename T>
void register_type ();

template<>
__attribute__((weak)) int get_type_id<int> () { return 0; }
template<>
__attribute__((weak)) int get_type_id<bool> () { return 1; }
template<>
__attribute__((weak)) int get_type_id<char> () { return 2; }

extern TypeRecord __start_calls_to_type;
extern TypeRecord __stop_calls_to_type;

#define CONCAT_RAW(a, b) a ## b
#define CONCAT(a, b) CONCAT_RAW(a, b)

#define NUMBER_PRIMTIVE_TYPES 3
#define REGISTER_TYPE(TYPE) \
    template<> \
    void register_type<TYPE> (); \
    static const TypeRecord CONCAT(record_, __LINE__) \
    __attribute__((section("calls_to_type"), used)) \
    = { &register_type<TYPE> }; \
    template<> \
    int get_type_id<TYPE> () { \
        return NUMBER_PRIMTIVE_TYPES + (int) (&CONCAT(record_, __LINE__) - &__start_calls_to_type); \
    } \
    template<> \
    void register_type<TYPE> () 

#define START_REGISTRATION(TYPE) printf(#TYPE " has id %d, total size %d\n", \
    get_type_id<TYPE>(), (int) sizeof(TYPE));
#define END_REGISTRATION(TYPE) printf("\n");
#define REGISTER_FIELD(TYPE, fieldType, field) \
    printf("  " #fieldType "(id=%d) " #field " at offset %d with size %d\n", \
        get_type_id<fieldType>(), \
        offsetof(TYPE, field), \
        (int) sizeof(fieldType) \
    );
