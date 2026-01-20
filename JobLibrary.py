import requests
import time
from robot.api.deco import keyword

class JobLibrary:    
    def __init__(self):
        self.session = requests.Session()

    @keyword
    def wait_for_job_completion(self, base_url, job_id, timeout=10):
        end_time = time.time() + float(timeout)
        
        while time.time() < end_time:
            response = self.session.get(f"{base_url}/job/{job_id}")
            response.raise_for_status()
            data = response.json()
            
            status = data.get("status")
            
            if status == "completed":
                return data
            elif status == "failed":
                raise AssertionError(f"Job failed: {data.get('error')}")
            
            time.sleep(0.5)
            
        raise AssertionError(f"Job {job_id} did not complete within {timeout} seconds.")

    @keyword
    def verify_matrix_size(self, complexity, matrix_string):
        expected_size = int(complexity) * 500
        expected_str = f"{expected_size}x{expected_size}"
        
        if matrix_string != expected_str:
            raise AssertionError(f"Expected size {expected_str}, got {matrix_string}")
        return True