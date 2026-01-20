import json
import uuid
from datetime import datetime
import redis
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


redis_client = redis.Redis(host='redis', port=6379, db=0)

class JobRequest(BaseModel):
    task_name: str
    complexity: int

@app.post("/submit-job")
def submit_job(job: JobRequest):
    job_id = str(uuid.uuid4())

    message = {
        "id": job_id,
        "task": job.task_name,
        "complexity": job.complexity,
        "submitted_at": str(datetime.now())

    }

    try:
        redis_client.lpush("hpc_queue", json.dumps(message))
        return {"job_id": job_id, "status": "queued"}
    except redis.ConnectionError:
        return {"error": "Could not connect to Redis"}
    
@app.get("/job/{job_id}")
def get_job_status(job_id: str):
    result = redis_client.get(job_id)
    
    if result is None:
        return {"job_id": job_id, "status": "pending (or invalid ID)"}
    
    return json.loads(result)
    
@app.get("/")
def health():
    return {"status": "API is ready"}