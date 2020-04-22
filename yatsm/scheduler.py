from apscheduler.events import (EVENT_ALL, EVENT_JOB_MAX_INSTANCES,
                                EVENT_JOB_SUBMITTED, JobSubmissionEvent)
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

jobstores = {"default": RedisJobStore(host="127.0.0.1", port=6379)}
executors = {
    "default": ThreadPoolExecutor(20),
}
job_defaults = {"max_instances": 4}

scheduler = AsyncIOScheduler(
    executors=executors, job_defaults=job_defaults, timezone=utc
)

submitted_jobs = {}


def events_processor(event):
    print(f">>>>> {event.__class__.__name__} <<<<<")
    if isinstance(event, JobSubmissionEvent):
        if event.code == EVENT_JOB_SUBMITTED:
            print(f"{event.job_id} - Submitted")
            submitted_jobs[event.job_id] = event
        elif event.code == EVENT_JOB_MAX_INSTANCES:
            print(f"{event.job_id} - Denied")


scheduler.add_listener(events_processor, EVENT_ALL)
