from fastapi import FastAPI
from fastapi.logger import logger

from yatsm.jobber import jobber
from yatsm.models import Job
from yatsm.scheduler import scheduler

app = FastAPI()

logger.info("Starting scheduler in background")
scheduler.start()


@app.post("/job")
async def add_job(job: Job):
    job = jobber.run_task(job, **job.task_args)
    return {"job_id": job.id}


@app.get("/job/{job_id}")
async def get_job(job_id: str):
    result = jobber.get_result(job_id)
    return {"job_id": job_id, **result}
