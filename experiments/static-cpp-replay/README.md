
# experiments/static-cpp-replay

This experiments shows the possibility to do something in a static way
and to generate an index associated with that. The purpose is to allow
to send a string over the network the first time and then to replace
it with a uuid. The benchmark shows capability of doing that with a few clock
cycles on average after the first run.

It also shows the possibility of replaying sending the string over the network.
It allows to request for a resynchronization in case of lost packets or reboot
of the other side.
