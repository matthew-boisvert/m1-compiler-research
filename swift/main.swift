import Dispatch


let queue = DispatchQueue.global()

let group = DispatchGroup()
group.enter()
queue.async(qos: .userInteractive) {
	let size = 10000
	let x = Array(repeating: 0, count: size)
	DispatchQueue.concurrentPerform(iterations: size) {
		let idx = ($0)
		var tmp = x[idx]
		for _ in 0...size {
			tmp = tmp + 1
		}
		//y[idx] = tmp
	}
	group.leave()
}
group.wait()
print("done")
