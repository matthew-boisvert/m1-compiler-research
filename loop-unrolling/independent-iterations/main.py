import os
import argparse

# Top of Swift file with includes and namespaces
top_source_string = """
import Foundation
import CoreFoundation
let SIZE = 1024 * 1024 * 8
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


# The reference function creates a loop that simply adds together all floating point constants in a loop
def reference_loop_source(chain_length, use_efficiency_cores):

    # function header
    function = "func reference_loop(b: UnsafeMutableBufferPointer<Float>, size: Int) -> Double {"
    # timing code
    time_counter = "  let duration = UnsafeMutablePointer<Double>.allocate(capacity: 1)"
    time_start = "  let start_time = CFAbsoluteTimeGetCurrent()"
    # loop header
    loop = "  for i in stride(from: 0, to: size - 1, by: 1) {"
    # read the original value from memory
    init = "    var tmp = b[i]"
    # create the dependency chain
    chain = []
    for i in range(0, chain_length):
      chain.append("    tmp += " + str(i+1)+".0")
    # store the final value to memory
    close = "    b[i] = tmp"
    # close loop and function
    loop_close = "  }"
    # finish timing
    time_end = "  duration.pointee = CFAbsoluteTimeGetCurrent() - start_time"
    ret = "  return duration.pointee"
    function_close = "}"
    # join together all the parts to make a complete function
    return function + "\n" + time_counter + "\n" + queue_operations([time_start, loop, init] + chain + [close, loop_close, time_end], use_efficiency_cores) + "\n" + ret + "\n" + function_close

# First hoomework function here! Implement the reference loop unrolled
# *sequentially*, That is, create dependency chains of length
# *chain_length*. Unroll the loop by a factor of *unroll_factor*. Do
# the unrolled loop iterations sequentially: i.e. do not start the
# chain of one iteration before the previous one is finished.

# to view the reference loop for a dependency chain of N, just
# run: python3 skeleton.py N 1.
# Your code will initially fail the assertion check, but you
# should be able to view the reference loop in homework.cpp.

# You can assume that the unroll factor evenly divides the
# array length. That is, you should be able to do this all
# in one loop without any extra clean-up loops.

# Don't forget! Floating point constants must have 'f' after them!
# that is, you would write 2 in floating point as '2.0f'
#
# You can gain confidence that implemented this correctly by executing
# skeleton.py with several power-of-two options for the unroll factor
# for example, try 1,2,4,8, etc.
def homework_loop_sequential_source(chain_length, unroll_factor, use_efficiency_cores):
    function = "func homework_loop_sequential(b: UnsafeMutableBufferPointer<Float>, size: Int) -> Double {"
    # timing code
    time_counter = "  let duration = UnsafeMutablePointer<Double>.allocate(capacity: 1)"
    time_start = "  let start_time = CFAbsoluteTimeGetCurrent()"

    tmp_init = []
     # Initialize variables at beginning (don't want to initialize in loop)
    for i in range(0, unroll_factor):
      tmp_init.append("  var tmp{0}: Float".format(i))
    # Iterate based on unroll factor
    loop_start = "  for i in stride(from: 0, to: size - 1, by: {0}) {{".format(unroll_factor) 
    chain = []
    # Sequentially perform updates on each unrolled variable
    for i in range(0, unroll_factor):
      chain.append("    tmp{0} = b[i + {0}]".format(i))
      for j in range(0, chain_length):
          chain.append("    tmp{0} += {1}.0".format(i, j+1))
      chain.append("    b[i + {0}] = tmp{0}".format(i))
    # close loop and function
    loop_close = "  }"
    # finish timing
    time_end = "  duration.pointee = CFAbsoluteTimeGetCurrent() - start_time"
    ret = "  return duration.pointee"
    function_close = "}"
    # join together all the parts to make a complete function
    return function + "\n" + time_counter + "\n" + queue_operations([time_start] + tmp_init + [loop_start] + chain + [loop_close, time_end], use_efficiency_cores) + "\n" + ret + "\n" + function_close

# Second homework function here! The specification for this
# function is the same as the first homework function, except
# this time you will interleave the instructions of the unrolled
# dependency chains.

# You can assume the unroll factor is a power of 2 and that the
# the dependency chain also a power of two. 
def homework_loop_interleaved_source(chain_length, unroll_factor, use_efficiency_cores):
    function = "func homework_loop_interleaved(b: UnsafeMutableBufferPointer<Float>, size: Int) -> Double {"
    # timing code
    time_counter = "  let duration = UnsafeMutablePointer<Double>.allocate(capacity: 1)"
    time_start = "  let start_time = CFAbsoluteTimeGetCurrent()"

    tmp_init = []
    # Initialize vars outside loop
    for i in range(0, unroll_factor):
        tmp_init.append("  var tmp{0}: Float".format(i))
    loop_start = "  for i in stride(from: 0, to: size - 1, by: {0}) {{".format(unroll_factor) 
    chain = []
    tmp_set = []
    # Interleave temp var initialization
    for i in range(0, unroll_factor):
        tmp_set.append("    tmp{0} = b[i + {0}]".format(i))
    # Interleave increments
    for i in range(0, chain_length):
        for j in range(0, unroll_factor):
            chain.append("    tmp{0} += {1}.0".format(j, i+1))
    # Interleave storing output values
    for i in range(0, unroll_factor):
        chain.append("    b[i + {0}] = tmp{0}".format(i))
    # close loop and function
    loop_close = "  }"
    # finish timing
    time_end = "  duration.pointee = CFAbsoluteTimeGetCurrent() - start_time"
    ret = "  return duration.pointee"

    function_close = "}"
    # join together all the parts to make a complete function
    return function + "\n" + time_counter + "\n" + queue_operations([time_start] + tmp_init + [loop_start] + tmp_set + chain + [loop_close, time_end], use_efficiency_cores) + "\n" + ret + "\n" + function_close

# String for the main function, including timings and
# reference checks.
main_source_string = """
// Sources:
//   https://stackoverflow.com/questions/25006235/how-to-benchmark-swift-code-execution
//   https://stackoverflow.com/questions/24755558/measure-elapsed-time-in-swift
func measure(block: (() -> Void)) -> Double {
  let start_time = CFAbsoluteTimeGetCurrent()
  block()
  return CFAbsoluteTimeGetCurrent() - start_time
}


func main() {
  var a: [Float32] = Array(stride(from: 0.0, through: Float(SIZE-1)*1.0, by: 1.0))
  var b: [Float32] = Array(stride(from: 0.0, through: Float(SIZE-1)*1.0, by: 1.0))
  var c: [Float32] = Array(stride(from: 0.0, through: Float(SIZE-1)*1.0, by: 1.0))

  // Source: https://developer.apple.com/documentation/swift/array/2994773-withunsafemutablebufferpointer
  // Why am I using unsafe mutable buffer pointers? Because
  // Swift is super strict about modifying captured variables
  // in closures and will murder me for attempting to change
  // an array in async
  let sequential_duration = a.withUnsafeMutableBufferPointer { buffer in 
    homework_loop_sequential(b: buffer, size: SIZE)
  }

  let interleaved_duration = c.withUnsafeMutableBufferPointer { buffer in 
    homework_loop_interleaved(b: buffer, size: SIZE)
  }

  let reference_duration = b.withUnsafeMutableBufferPointer { buffer in
    reference_loop(b: buffer, size: SIZE)
  }

  print(String(format: "sequential loop time: %f", sequential_duration));
  print(String(format: "interleaved loop time: %f", interleaved_duration));
  print(String(format: "reference loop time: %f", reference_duration));
  print("----")
  print("speedups:")
  print(String(format: "sequential speedup over reference: %f", reference_duration / sequential_duration))
  print(String(format: "interleaved speedup over reference: %f", reference_duration / interleaved_duration))
}

main()
"""

# Create the program source code
def pp_program(chain_length, unroll_factor, use_efficiency_cores):

    # Your two functions are called here
    homework_source_string_sequential = homework_loop_sequential_source(chain_length, unroll_factor, use_efficiency_cores)
    homework_source_string_interleaved = homework_loop_interleaved_source(chain_length, unroll_factor, use_efficiency_cores)

    # join together all the other parts to make a complete C++ program
    return "\n".join([top_source_string, reference_loop_source(chain_length, use_efficiency_cores), homework_source_string_sequential, homework_source_string_interleaved, main_source_string])

# Write a string to a file (helper function)
def write_str_to_file(st, fname):
    f = open(fname, 'w')
    f.write(st)
    f.close()

# Compile the program. Don't change the options here for the official
# assignment submission. Feel free to change them for your own curiosity.
# Some notes:
#
# I am using a recent version of C++ to use the chrono library.
#
# I am disabling the compiler's loop unrolling so we can ensure the
# reference loop and the homework loops are not unrolled "behind our backs"
#
# I am using the lowest optimization level here (-O0) to disable most
# optimizations. The compiler does some really ticky things even at
# (-O1) here. 
def compile_program():
    cmd = "swiftc -Onone -o homework homework.swift"
    print("running: " + cmd)
    assert(os.system(cmd) == 0)

# Execute the program
def run_program():
    cmd = "./homework"
    print("running: " + cmd)
    print("")
    assert(os.system(cmd) == 0)

def generate_and_run(chain_length, unroll_factor, use_efficiency_cores):
    print("")
    print("----------")
    print("generating and running for:")
    print("chain length = " + str(chain_length))
    print("unroll factor = " + str(unroll_factor))
    print("use efficiency cores = " + str(use_efficiency_cores))
    print("-----")
    print("")
    
    program_str = pp_program(chain_length, unroll_factor, use_efficiency_cores)
    write_str_to_file(program_str, "homework.swift")
    compile_program()
    run_program()

# gets two command line args, chain length (CL) and unroll factor (UF)
def main():
    parser = argparse.ArgumentParser(description='Exploiting ILP by unrolling independent loops.')
    parser.add_argument('chain_length', metavar='CL', type=int,
                   help='the length of dependent instructions per loop iteration to generate')
    parser.add_argument('unroll_factor', metavar='UF', type=int,
                   help='how many loop iterations to unroll')
    parser.add_argument('use_efficiency_cores', metavar='UEC', type=int,
                   help='1 for efficiency cores, 0 for power cores')
    args = parser.parse_args()
    CL = args.chain_length
    UF = args.unroll_factor
    use_efficiency_cores = args.use_efficiency_cores
    generate_and_run(CL, UF, use_efficiency_cores)

if __name__ == "__main__":
    main()
