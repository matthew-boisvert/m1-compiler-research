#include <iostream>
#include <assert.h>
#include <chrono>
#include <thread>
#include <math.h>

#define SIZE 1000000000
#define TERM 1000000.0

using namespace std;
using namespace chrono;

void log_array(volatile double* a, volatile double* b, int size, int tid, int num_threads) {
	auto start = high_resolution_clock::now();
	int indices_per_thread = size / num_threads;
	for (int i = tid * indices_per_thread; i < ((tid + 1) * indices_per_thread); i++) {
		b[i] = log(a[i]);
	}
	auto end = high_resolution_clock::now();
	auto duration = duration_cast<nanoseconds>(end - start);
	double seconds = duration.count()/1000000000.0;
	cout << "Seconds elapsed on thread " << tid << ": " << seconds << endl;
	return;
}


int main(int argc, char** argv)
{
	int num_threads = 8;
	if (argc == 2) {
		num_threads = atoi(argv[1]);
	}
	thread thread_arr[num_threads];
	double *a = (double *) malloc(SIZE * sizeof(double));
	double *b = (double *) malloc(SIZE * sizeof(double));
	
	for (int i = 0; i < SIZE; i++) {
		a[i] = b[i] = TERM;
	}
	auto start = high_resolution_clock::now();
	for (int i = 0; i < num_threads; i++) {
		thread_arr[i] = thread(log_array, a, b, SIZE, i, num_threads);
	}
	for (int i = 0; i < num_threads; i++) {
		thread_arr[i].join();
	}
	auto end = high_resolution_clock::now();	
	for (int i = 0; i < SIZE; i++) {
		assert(b[i] == log(a[i]));
	}
	auto duration = duration_cast<nanoseconds>(end - start);
	double seconds = duration.count()/1000000000.0;
	cout << "Total seconds elapsed: " << seconds << endl;	
	return 0;
}
