
#include <iostream>
#include "manager.h"

struct MyType {
    int id;
    bool enabled;
};

REGISTER_TYPE(MyType) {
    START_REGISTRATION(MyType);
    REGISTER_FIELD(MyType, int, id);
    REGISTER_FIELD(MyType, bool, enabled);
    END_REGISTRATION(MyType);
}

struct MyType2 {
    bool enabled;
    int id;
};

REGISTER_TYPE(MyType2) {
    START_REGISTRATION(MyType2);
    REGISTER_FIELD(MyType2, int, id);
    REGISTER_FIELD(MyType2, bool, enabled);
    END_REGISTRATION(MyType2);
}
