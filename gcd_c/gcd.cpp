#include <stdio.h>
#include <stdlib.h>
#include <dispatch/dispatch.h>

void increment_kernel (int* x, int* y, int* n) {
  // concurrent queue
  dispatch_queue_t my_queue = dispatch_get_global_queue(QOS_CLASS_BACKGROUND, 0);

  // for loop: add large number to each element of x and store result in y
  dispatch_apply (*n, my_queue, ^(size_t idx){
      int tmp = x[idx];
      for( int j = 0; j < 10000; j++) {
	tmp++;
      }
      //y[idx] = tmp;
  });
}

int
main(int argc, char *argv[])
{
	int n = 10000;
  	int x[n];
  	int y[n];
	for (int i = 0; i < n; i++) {
		x[i] = y[i] = 1;
	}
	increment_kernel(x, y, &n);
	printf("%d\n", y[100]);
	return 0;
}
