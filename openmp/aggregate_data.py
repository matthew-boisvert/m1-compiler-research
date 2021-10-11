import subprocess
import sys
import statistics

mutexFiles = {
    "C++ Mutex": "./cpp_mutex",
    "Bakery Mutex": "./bakery_mutex",
    "Filter Mutex": "./filter_mutex"
}

times = dict()

if __name__ == "__main__":
	num_tests = 5
	max_threads = 16
	timing_stats = dict()
	if len(sys.argv) == 3:
		max_threads = int(sys.argv[1])
		num_tests = int(sys.argv[2])
	current_threads = 1
	
	while (current_threads <= max_threads):
		print("Current threads: {0}".format(current_threads))
		for i in range(0, num_tests):
			output = subprocess.run(["./log_threads", str(current_threads)], stdout=subprocess.PIPE).stdout.decode('utf-8')
			print(output)
			executionTimes = []
			for line in output.split("\n"):
				if line.startswith("Seconds"):
					executionTimes.append(float(line.split(":")[1]))
			average = statistics.mean(executionTimes)
			var = None
			if len(executionTimes) > 1:
				var = statistics.variance(executionTimes)
			if current_threads not in times:
				timing_stats[current_threads] = {"means": [], "vars": []}
			timing_stats[current_threads]["means"].append(average)
			if len(executionTimes) > 1:
				timing_stats[current_threads]["vars"].append(var)
		current_threads = current_threads * 2
	print(timing_stats)
	for thread_count in timing_stats:
		avg_mean = statistics.mean(timing_stats[thread_count]["means"])
		avg_var = None
		if thread_count > 1:
			avg_var = statistics.mean(timing_stats[thread_count]["vars"])
		print("Thread {0}: Average mean = {1}, average var = {2}".format(thread_count, avg_mean, avg_var))

