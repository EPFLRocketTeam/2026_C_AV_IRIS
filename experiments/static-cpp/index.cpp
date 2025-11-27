#include <bits/stdc++.h>

using namespace std;

template<typename T>
double benchmark(T f, int repetitions) {
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < repetitions; i ++) {
        f();
    }

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();

    return duration / ((double) repetitions);
}

volatile int result  = 0;
volatile int content = 0;

int do_something_statically () {
    static int val = ([]() {
        // this happens at most once
        return content ++;
    })();

    result = val;
    return result;
}

int main () {
    std::cout << "RUNNING BENCHMARKS FOR 'static-cpp' (over 1'000'000 calls)" << std::endl;
    double duration = benchmark(do_something_statically, 1'000'000);
    std::cout << " Average number of nanoseconds " << std::fixed << std::setprecision(5) << duration << "\n";
}