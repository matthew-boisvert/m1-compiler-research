import Foundation
import CoreFoundation
let SIZE = 1024 * 1024 * 8

func mem_access_kernel(ptr_array: UnsafeMutableBufferPointer<UnsafeMutablePointer<Float32>>, size: Int, use_efficiency_cores: Bool) -> Double {
    let duration = UnsafeMutablePointer<Double>.allocate(capacity: 1)
    let queue = DispatchQueue.global()
    let group = DispatchGroup()
    group.enter()
    let qos = (use_efficiency_cores ? DispatchQoS.background : DispatchQoS.userInteractive)
    queue.async(qos: qos) {
        let start_time = CFAbsoluteTimeGetCurrent()
        for i in stride(from: 0, to: size - 1, by: 1) {
            let ptr = ptr_array[i]
            ptr.pointee = ptr.pointee + 1.0
        }
        duration.pointee = CFAbsoluteTimeGetCurrent() - start_time
        group.leave()
    }
    group.wait()
    return duration.pointee
}

func main() {
    let use_efficiency_cores = CommandLine.arguments[1]
    var a: [Float32] = Array(stride(from: 0.0, through: Float(SIZE-1)*1.0, by: 1.0))
    var b: [UnsafeMutablePointer<Float32>] = Array()
    for i in stride(from: 0, to: SIZE - 1, by: 1) {
        withUnsafeMutablePointer(to: &a[i]) { p in
            b.append(p)
        }
    }
    let duration = b.withUnsafeMutableBufferPointer { buffer in
        mem_access_kernel(ptr_array: buffer, size: SIZE, use_efficiency_cores: Bool(use_efficiency_cores) ?? false)
    }
    print(String(format: "duration: %f", duration));
}

main()
