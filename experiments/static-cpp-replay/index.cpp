#include <bits/stdc++.h>

using namespace std;

template<typename T>
pair<double, double> benchmark(T f, int repetitions) {
    
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

    return make_pair((double)duration1, duration / ((double) repetitions));
}

volatile int result  = 0;
volatile int content = 0;

std::function<void(void)> to_replay[2];
size_t num_replay = 0;
void run_and_buffer_for_replay (std::function<void(void)> fnc) {
    to_replay[num_replay ++] = fnc;
    fnc();
}
void replay () {
    for (int i = 0; i < num_replay; i ++) to_replay[i]();
}

template<const char* F>
int do_something_statically () {
    static int val = ([]() {
        static int res = content ++;

        run_and_buffer_for_replay([] {
            // this happens at most once and can be replayed
            // it also reuses the value res.
            std::cout << F << " WITH ID " << res << "\n";
        });

        return res;
    })();

    result = val;
    return result;
}

static const char MESSAGE1[] = "log type 1";
static const char MESSAGE2[] = "log type 2";

int main () {
    std::cout << "RUNNING BENCHMARKS FOR 'static-cpp-replay' (twice over 10'000'000 calls)" << std::endl;
    auto [start1, duration1] = benchmark(do_something_statically<MESSAGE1>, 10'000'000);
    auto [start2, duration2] = benchmark(do_something_statically<MESSAGE2>, 10'000'000);

    std::cout << std::endl;
    std::cout << " Startup number of nanoseconds (1) " << std::fixed << std::setprecision(5) << start1 << "\n";
    std::cout << " Startup number of nanoseconds (2) " << std::fixed << std::setprecision(5) << start2 << "\n";
    std::cout << std::endl;
    std::cout << " Average number of nanoseconds (1) " << std::fixed << std::setprecision(5) << duration1 << "\n";
    std::cout << " Average number of nanoseconds (2) " << std::fixed << std::setprecision(5) << duration2 << "\n";
    std::cout << std::endl;

    std::cout << "REPLAY STATIC PART" << std::endl;
    replay();
}