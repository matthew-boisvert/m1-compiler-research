import Dispatch
import Foundation
import CoreFoundation

func increment(x: inout [Double], size: Int, tid: Int, threads: Int) {
    let indices_per_thread = size / threads
    let lower_bound = tid * indices_per_thread
    let upper_bound = (tid+1) * indices_per_thread
    for i in lower_bound...upper_bound-1 {
        var tmp = x[i]
        for _ in 0...1000000*10 {
            tmp = tmp + 1.0
        }
        x[i] = tmp
    }
}

func increment_kernel(threads: Int, use_efficiency_cores: Bool) -> Double {
    let queue = DispatchQueue.global()
    let group = DispatchGroup()
    let n = 4096
    var x: [Double]  = Array(repeating: 1, count: n)
    let duration = UnsafeMutablePointer<Double>.allocate(capacity: 1)
    let qos = (use_efficiency_cores ? DispatchQoS.background : DispatchQoS.userInteractive)
    group.enter()
    queue.async(qos: qos) {
        let start_time = CFAbsoluteTimeGetCurrent()
        DispatchQueue.concurrentPerform(iterations: threads) {
            let tid = ($0)
            increment(x: &x, size: n, tid: tid, threads: threads)
        }
        duration.pointee = CFAbsoluteTimeGetCurrent() - start_time
        group.leave()
    }
    group.wait()
    return duration.pointee
}

func main() {
    let threads = CommandLine.arguments[1]
    let use_efficiency_cores = CommandLine.arguments[2]
    let duration = increment_kernel(threads: Int(threads) ?? 1, use_efficiency_cores: Bool(use_efficiency_cores) ?? false)
    print(String(format: "duration: %f", duration))
}

main()
