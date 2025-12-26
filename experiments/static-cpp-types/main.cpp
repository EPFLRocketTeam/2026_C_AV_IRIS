
#include <iostream>
#include "manager.h"

int main () {
    printf("--- Statically Found Types ---\n");
    for (TypeRecord* it = &__start_calls_to_type; it < &__stop_calls_to_type; it ++) {
        void (*func) () = it->registerFunction;

        func();
    }
}
