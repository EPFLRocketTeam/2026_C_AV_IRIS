
#include <bits/stdc++.h>

#include "manager.h"

// BENCHMARK

template<typename T>
std::pair<double, double> benchmark(T f, int repetitions) {
    auto start1 = std::chrono::high_resolution_clock::now();
    f();
    auto end1 = std::chrono::high_resolution_clock::now();
    auto duration1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count();

    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < repetitions; i ++) {
        f();
    }

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();

    return std::make_pair((double)duration1, duration / ((double) repetitions));
}

volatile int result;
int do_it_statically () {
    static int val = _InternalStringToIndex("Benchmark, World !");
    result = val;

    return val;
}

// EXAMPLE

void ShowAllCalls() {
    std::cout << std::endl;
    std::cout << "--- Statically Found All Calls ---" << std::endl;
    int index = 0;
    for (const CallRecord* it = &__start_calls; it < &__stop_calls; ++it) {
        std::cout << "INDEX " << index << ": ";
        std::cout << it->message << " at " << it->file << ":" << it->line << std::endl;

        index ++;
    }
    std::cout << std::endl;
}

void UnreachableFunction () {
    int i1 = StringToIndex("Never, World !");
}

int main () {
    std::cout << "=== " << "EXAMPLE" << std::endl;
    // Some stuff that did happen
    int i1 = StringToIndex("Hello, World !");

    ShowAllCalls();

    // Some stuff that happens after
    int i2 = StringToIndex("Bye, World !");

    std::cout << std::endl;
    std::cout << std::endl;
    std::cout << std::endl;
    
    std::cout << "RUNNING BENCHMARKS FOR 'static-cpp-all-available' (1'000'000 calls)" << std::endl;
    auto [start1, duration1] = benchmark(do_it_statically, 1'000'000);
    
    std::cout << std::endl;
    std::cout << " Startup number of nanoseconds " << std::fixed << std::setprecision(5) << start1 << "\n";
    std::cout << " Average number of nanoseconds " << std::fixed << std::setprecision(5) << duration1 << "\n";
    std::cout << std::endl;
}
