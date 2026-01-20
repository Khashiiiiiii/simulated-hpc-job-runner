import redis
import json
import time
import numpy as np
import sys

try:
    r = redis.Redis(host='redis', port=6379, db=0)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)


def perform_heavy_computation(job_data):
    job_id = job_data['id']
    print(f" [x] Received Job {job_data['id']}")
    complexity = job_data['complexity']

    if complexity > 20:
        print(f" [!] Job {job_data['id']} rejected: Complexity too high.")
        return
    
    size = complexity * 500
    print(f"Processing matrix size {size}x{size}...")
    
    start = time.time()
    matrix_a = np.random.rand(size, size)
    matrix_b = np.random.rand(size, size)
    _ = np.dot(matrix_a, matrix_b)
    duration = time.time() - start
    
    print(f" [x] Job {job_data['id']} Done in {duration:.4f}s")

    result_data = {
        "status": "completed",
        "job_id": job_id,
        "duration_seconds": duration,
        "matrix_size": f"{size}x{size}",
        "processed_at": str(time.ctime())
    }
    
    r.set(job_id, json.dumps(result_data))

print(' [*] Worker Node Started. Waiting for jobs...')

while True:
    _, data = r.brpop("hpc_queue", 0)
    
    job_data = json.loads(data)
    perform_heavy_computation(job_data)