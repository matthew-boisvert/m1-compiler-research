import os
import argparse

# Top of Swift file with includes and namespaces
top_source_string = """
import Foundation
import CoreFoundation
let SIZE = 1024 * 1024 * 8
typealias reduce_type = Double
"""

# Create async closure surrounding sequence of instructions
def queue_operations(actions_list, use_efficiency_cores):
    # Creating reference to global dispatch queue in order
    # to run actions asynchronously
    queue = "let queue = DispatchQueue.global()"
    group = "let group = DispatchGroup()"
    # Group is used to wait for async to finish. Of course,
    # this defeats the purpose of async in this context
    # but we need async so that we can specify the qos
    enter = "group.enter()"
    queue_async = ""
    if use_efficiency_cores:
      queue_async = "queue.async(qos: .background) {"
    else:
      queue_async = "queue.async(qos: .userInteractive) {"
    leave = "  group.leave()"
    queue_end = "}"
    wait = "group.wait()"
    # Create string with async closure
    op_list = [queue, group, enter, queue_async] + actions_list + [leave, queue_end, wait]
    for i in range(0, len(op_list)):
      op_list[i] = "  " + op_list[i] 
    return "\n".join(op_list) 


# The reference loop simply adds together all elements in the array
def reference_reduction_source(use_efficiency_cores):

    # function header
    function = "func reference_reduction(b: UnsafeMutableBufferPointer<reduce_type>, size: Int) -> Double {"
    # timing code
    time_counter = "  let duration = UnsafeMutablePointer<Double>.allocate(capacity: 1)"
    time_start = "  let start_time = CFAbsoluteTimeGetCurrent()"

    # loop header
    loop = "  for i in 1...(size-1) {"

    #simple reduction equation
    eq = "    b[0] += b[i];"

    # closing braces
    loop_close = "  }"
    # finish timing
    time_end = "  duration.pointee = CFAbsoluteTimeGetCurrent() - start_time"
    ret = "  return duration.pointee"

    function_close = "}"

    # joining together all parts
    return function + "\n" + time_counter + "\n" + queue_operations([time_start, loop, eq, loop_close, time_end], use_efficiency_cores) + "\n" + ret + "\n" + function_close

# Your homework will largely take place here. Create a loop that
# is semantically equivalent to the reference loop. That is, it computes
# a[0] = a[0] + a[1] + a[2] + a[3] + a[4] ... + a[size]
#
# where size is passed in by the main source string.
#
# You should unroll by a factor of "partitions". This is done logically
# by splitting a into N partitions (where N == partitions). You will compute
# N reductions, one computation for each partition per loop iteration.
#
# You will need a cleanup loop after the main loop to combine
# the values in each partition.
#
# You can assume the size and the number of partitions will be
# a power of 2, which should make the partitioning logic simpler.
#
# You can gain confidence in your solution by running the code
# with several power-of-2 unroll factors, e.g. 2,4,8,16. You
# should pass the assertion in the code.
#
# You can assume partition is less than size.
def homework_reduction_source(partitions, use_efficiency_cores):
    # header
    function = "func homework_reduction(b: UnsafeMutableBufferPointer<reduce_type>, size: Int) -> Double {"
    # timing code
    time_counter = "  let duration = UnsafeMutablePointer<Double>.allocate(capacity: 1)"
    time_start = "  let start_time = CFAbsoluteTimeGetCurrent()"
    init_var = "  let partitionSize = size / {0}".format(partitions)
    # Create main loop which performs reduction on partitions
    main_loop_start = "  for i in 1...(partitionSize-1) {"
    main_chain = []
    # Perform index updates for every partition
    for j in range(0, partitions):
        idx = "{0} * partitionSize".format(j)
        main_chain.append("    b[{0}] += b[({0}) + i];".format(idx))
    main_loop_close = "  }"
    # Coalesce all of the partition results into a[0]
    cleanup_loop_start = "  for i in stride(from: partitionSize, to: size - 1, by: partitionSize) {"
    cleanup_loop_body = "    b[0] += b[i];"
    cleanup_loop_close = " }"
    # finish timing
    time_end = "  duration.pointee = CFAbsoluteTimeGetCurrent() - start_time"
    ret = "  return duration.pointee"
    # Combine strings to create function
    function_close = "}"
    return function + "\n" + time_counter + "\n" + queue_operations([time_start, init_var, main_loop_start] + main_chain + [main_loop_close, cleanup_loop_start, cleanup_loop_body, cleanup_loop_close, time_end], use_efficiency_cores) + "\n" + ret + "\n" + function_close


# String for the main function, including timings and
# reference checks.
main_source_string = """
// Sources:
//   https://stackoverflow.com/questions/25006235/how-to-benchmark-swift-code-execution
//   https://stackoverflow.com/questions/24755558/measure-elapsed-time-in-swift
//   Divine intervention
func measure(block: (() -> Void)) -> Double {
  let start_time = CFAbsoluteTimeGetCurrent()
  block()
  return CFAbsoluteTimeGetCurrent() - start_time
}


func main() {
  var a: [reduce_type] = Array(repeating: 1.0, count: SIZE)
  var b: [reduce_type] = Array(repeating: 1.0, count: SIZE)

  // Source: https://developer.apple.com/documentation/swift/array/2994773-withunsafemutablebufferpointer
  // Why am I using unsafe mutable buffer pointers? Because
  // Swift is super strict about modifying captured variables
  // in closures and will murder me for attempting to change
  // an array in async
  let hw_reduction_duration = a.withUnsafeMutableBufferPointer { buffer in 
    homework_reduction(b: buffer, size: SIZE)
  }

  let reference_duration = b.withUnsafeMutableBufferPointer { buffer in 
    reference_reduction(b: buffer, size: SIZE)
  }

  print(String(format: "new loop time: %f", hw_reduction_duration))
  print(String(format: "reference loop time: %f", reference_duration))
  print(String(format: "speedup: %f", reference_duration / hw_reduction_duration))
}

main()
"""

# Create the program source code
def pp_program(partitions, use_efficiency_cores):

    # Your function is called here
    homework_string = homework_reduction_source(partitions, use_efficiency_cores)

    # View your homework source string here for debugging
    return "\n".join([top_source_string, reference_reduction_source(use_efficiency_cores), homework_string, main_source_string])

# Write a string to a file (helper function)
def write_str_to_file(st, fname):
    f = open(fname, 'w')
    f.write(st)
    f.close()

# Compile the program. Don't change the options here for the official
# assignment report. Feel free to change them for your own curiosity.
# Some notes:
#
# I am using a recent version of C++ to use the chrono library.
#
# I am disabling the compiler's loop unrolling so we can ensure the
# reference loop and the homework loops are not unrolled "behind our backs"
#
# I am using the highest optimization level (-O3) to illustrate that
# the compiler is not even brave enough to perform this optimization!
def compile_program():
    cmd = "swiftc -Onone -o homework homework.swift"
    print("running: " + cmd)
    assert(os.system(cmd) == 0)

# Run the program
def run_program():
    cmd = "./homework"
    print("running: " + cmd)
    print("")
    assert(os.system(cmd) == 0)

# This is the top level program function. Generate the C++ program,
# compile it, and run it.
def generate_and_run(partitions, use_efficiency_cores):
    print("")
    print("----------")
    print("generating and running for:")
    print("partitions = " + str(partitions))
    print("use efficiency cores = " + str(use_efficiency_cores))
    print("-----")
    print("")

    # get the C++ source
    program_str = pp_program(partitions, use_efficiency_cores)

    # write it to a file (homework.swift)
    write_str_to_file(program_str, "homework.swift")

    # compile the program
    compile_program()

    # run the program
    run_program()

# gets one command line arg unroll factor (UF)                                               
def main():
    parser = argparse.ArgumentParser(description='Part 2 of Homework 1: exploiting ILP by unrolling reduction loop iterations.')
    parser.add_argument('unroll_factor', metavar='UF', type=int,
                   help='how many loop iterations to unroll')
    parser.add_argument('use_efficiency_cores', metavar='UEC', type=int,
                   help='1 for efficiency cores, 0 for power cores')
    args = parser.parse_args()
    UF = args.unroll_factor
    use_efficiency_cores = args.use_efficiency_cores
    generate_and_run(UF, use_efficiency_cores)

if __name__ == "__main__":
    main()
