#include <iostream>
#include <assert.h>
#include <chrono>

#define SIZE 1000000000
#define TERM 1000000

using namespace std;
using namespace chrono;

int main()
{
	int *a = (int *) malloc(SIZE * sizeof(int));
	int *b = (int *) malloc(SIZE * sizeof(int));
	int *c = (int *) malloc(SIZE * sizeof(int));
	
	for (int i = 0; i < SIZE; i++) {
		a[i] = b[i] = TERM;
	}
	auto start = high_resolution_clock::now();
	#pragma omp parallel for
	for (int i = 0; i < SIZE; i++) {
		//if (omp_get_thread_num() == 0) {
			c[i] = a[i] + b[i];
		//}
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
