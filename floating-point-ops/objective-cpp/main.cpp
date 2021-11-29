#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <chrono>
#include <iostream>
#include <dispatch/dispatch.h>

using namespace std;
using namespace std::chrono;

void increment (float* x, float* y, int n, size_t tid, const int num_threads) {
    int indices_per_thread = (n / num_threads);
    for (int i = tid * indices_per_thread; i < (tid + 1) * indices_per_thread; i++) {
      float tmp = x[i];
      for (int j = 0; j < 1000000*10; j++) {
        tmp += 1.0f;
      }
      x[i] = tmp;
    }
}

float increment_kernel (float* x, float* y, int n, int threads, bool use_efficiency_cores) {
    int qos = (use_efficiency_cores ? QOS_CLASS_BACKGROUND : QOS_CLASS_USER_INTERACTIVE); 
    dispatch_queue_t my_queue = dispatch_get_global_queue(qos, 0);
    auto start = high_resolution_clock::now();
    dispatch_apply (threads, my_queue, ^(size_t idx){
      increment(x, y, n, idx, threads);
    });
    auto end = high_resolution_clock::now();
    auto duration = duration_cast<nanoseconds>(end - start);
    float seconds = duration.count()/1000000000.0;
    return seconds;
}

int main(int argc, char *argv[]) {
    int num_threads = atoi(argv[1]);
    int n = 4096;
    float x[n];
    float y[n];
    for (int i = 0; i < n; i++) {
        x[i] = y[i] = 1;
    }
    bool use_efficiency_cores = (strcmp(argv[2], "true") == 0);
    float duration = increment_kernel(x, y, n, num_threads, use_efficiency_cores);
    cout << "duration: " << duration << endl;
    return 0;
}
