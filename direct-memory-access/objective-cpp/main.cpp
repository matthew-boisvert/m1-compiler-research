#include <stdio.h>
#include <stdlib.h>
#include <dispatch/dispatch.h>
#include <time.h>
#include <chrono>
#include <iostream> 
#define SIZE 1024 * 1024 * 8

using namespace std;
using namespace std::chrono;

float mem_access_kernel (float** ptr_array, int size, bool use_efficiency_cores) {
    __block float seconds = 0;
    int qos = (use_efficiency_cores ? QOS_CLASS_BACKGROUND : QOS_CLASS_USER_INTERACTIVE); 
    dispatch_queue_t queue = dispatch_get_global_queue(qos, 0);
    dispatch_group_t group = dispatch_group_create();
    dispatch_group_enter(group);
    dispatch_async(queue, ^{
        auto start = high_resolution_clock::now();
        for (int i = 0; i < size; i++) {
            float* ptr = ptr_array[i];
            (*ptr) = (*ptr) + 1.0f;
        }
        auto end = high_resolution_clock::now();
        auto duration = duration_cast<nanoseconds>(end - start);
        seconds = duration.count()/1000000000.0;
        dispatch_group_leave(group);
    });
    dispatch_group_wait(group, DISPATCH_TIME_FOREVER);
    return seconds;
}

int main(int argc, char *argv[]) {
    srand (time(NULL));
    float* a = (float*)malloc(sizeof(float) * SIZE);
    float** b = (float**)malloc(sizeof(float*) * SIZE);
    for (int i = 0; i < SIZE; i++) {
        a[i] = i;
    }
    for (int i = 0; i < SIZE; i++) {
        b[i] = &a[i];
    }
    bool use_efficiency_cores = (strcmp(argv[1], "true") == 0);
    float duration = mem_access_kernel(b, SIZE, use_efficiency_cores);
    cout << "duration: " << duration << endl;
    return 0;
}
