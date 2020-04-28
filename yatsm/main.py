import inspect
from datetime import timedelta

from dramatiq import Actor
from fastapi import Depends, FastAPI, HTTPException
from fastapi.logger import logger
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from yatsm import auth, jobs, models
from yatsm.jobber import jobber
from yatsm.scheduler import scheduler

app = FastAPI()

logger.info("Starting scheduler in background")
scheduler.start()

available_jobs = {}

excludes = ["success", "failure"]


@app.on_event("startup")
async def get_available_jobs():
    available_jobs.update(
        {
            j: str(inspect.signature(getattr(jobs, j).fn))
            for j in dir(jobs)
            if isinstance(getattr(jobs, j), Actor) and j not in excludes
        }
    )


@app.post("/job")
async def add_job(
    job: models.Job, current_user: models.User = Depends(auth.get_current_active_user)
):
    job = jobber.run_task(job)
    return {"job_id": job.id}


@app.get("/job/{job_id}")
async def get_job(
    job_id: str, current_user: models.User = Depends(auth.get_current_active_user)
):
    result = jobber.get_result(job_id)
    return {"job_id": job_id, "results": result}


@app.get("/jobs/available")
async def get_job():
    print("available")
    return available_jobs


@app.post("/token", response_model=models.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(
        auth.fake_users_db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
