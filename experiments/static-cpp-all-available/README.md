
# experiments/static-cpp-all-avaible

This experiments shows the possibility to setup a function in a static way so that
the main loop is aware of all calls to that function and their arguments. The
arguments should all be static and can't be pointers (e.g. default ints or
strings in brackets so it can be stored in a local array).

Such a thing generates absolutely zero overhead. It remains to be checked if it is
possible for such a program to be used on stm32 or microcontrollers in general as
this starts to become obscure features of the compiler/linker.
