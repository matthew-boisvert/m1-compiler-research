#include <iostream>
#include <assert.h>
#include <chrono>
#include <thread>

#define SIZE 1000000000
#define THREADS 1
#define TERM 1000000

using namespace std;
using namespace chrono;

void add(volatile int* a, volatile int* b, volatile int* c, int size, int tid, int num_threads) {
	auto start = high_resolution_clock::now();
	int indices_per_thread = size / num_threads;
	for (int i = tid * indices_per_thread; i < ((tid + 1) * indices_per_thread); i++) {
		c[i] = a[i] + b[i];
	}
	auto end = high_resolution_clock::now();
	auto duration = duration_cast<nanoseconds>(end - start);
	double seconds = duration.count()/1000000000.0;
	cout << "Thread " << tid << " took " << seconds << " seconds" << endl;
	return;
}


int main()
{
	thread thread_arr[THREADS];
	int *a = (int *) malloc(SIZE * sizeof(int));
	int *b = (int *) malloc(SIZE * sizeof(int));
	int *c = (int *) malloc(SIZE * sizeof(int));
	
	for (int i = 0; i < SIZE; i++) {
		a[i] = b[i] = TERM;
	}
	auto start = high_resolution_clock::now();
	for (int i = 0; i < THREADS; i++) {
		thread_arr[i] = thread(add, a, b, c, SIZE, i, THREADS);
	}
	for (int i = 0; i < THREADS; i++) {
		thread_arr[i].join();
	}
	auto end = high_resolution_clock::now();	
	for (int i = 0; i < SIZE; i++) {
		assert(c[i] == (TERM * 2));
	}
	auto duration = duration_cast<nanoseconds>(end - start);
	double seconds = duration.count()/1000000000.0;
	cout << "Seconds elapsed: " << seconds << endl;	
	return 0;
}
