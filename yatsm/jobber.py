from uuid import UUID, uuid4

from apscheduler.job import Job
from apscheduler.triggers.combining import AndTrigger, OrTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from yatsm import jobs, models
from yatsm.db import db, deserialize
from yatsm.models import ScheduleOptions
from yatsm.scheduler import scheduler


def trigger_factory(trigger_data):
    """
    Esse factory já considera que os dados foram sanitizados
    """
    combine_options = {"AND": AndTrigger, "OR": OrTrigger}
    trigger_options = {"IntervalTrigger": IntervalTrigger, "CronTrigger": CronTrigger}
    trigger_params = [
        trigger_options.get(t["name"])(**t["kwargs"]) for t in trigger_data["triggers"]
    ]
    return combine_options.get(trigger_data["combine"])(trigger_params)


class BackgroundJobs:
    def __init__(self):
        self.tasks = {}
        self._scheduler = scheduler

    def generate_uid(self) -> UUID:
        return uuid4()

    def default_task_options(self) -> dict:
        return {
            "on_success": jobs.success,
            "on_failure": jobs.failure,
            "message_id": str(self.generate_uid()),
        }

    @staticmethod
    def get_job_ref(name):
        return getattr(jobs, name)

    def run_task_interval(self, job) -> Job:
        task = BackgroundJobs.get_job_ref(job.task_name)
        interval_args = {k: v for k, v in job.interval_options.dict().items() if v}
        tsk_kwargs = {"kwargs": job.task_args, **self.default_task_options()}
        if job.meta_data:
            tsk_kwargs.update({**job.meta_data})
        job = self._scheduler.add_job(
            task.send_with_options,
            kwargs=tsk_kwargs,
            replace_existing=True,
            id=tsk_kwargs["message_id"],
            trigger="interval",
            **interval_args
        )
        self.tasks[tsk_kwargs["message_id"]] = job
        return job

    def run_task_cron(self, job) -> Job:
        task = BackgroundJobs.get_job_ref(job.task_name)
        cron_args = {k: v for k, v in job.cron_options.dict().items() if v}
        if "expression" in cron_args:
            trigger = CronTrigger.from_crontab(cron_args.pop("expression"))
        else:
            trigger = "cron"
        tsk_kwargs = {"kwargs": job.task_args, **self.default_task_options()}
        if job.meta_data:
            tsk_kwargs.update({**job.meta_data})
        job_params = dict(
            kwargs=tsk_kwargs,
            replace_existing=True,
            id=tsk_kwargs["message_id"],
            trigger=trigger,
        )
        if isinstance(trigger, str):
            job_params.update(**cron_args)
        job = self._scheduler.add_job(task.send_with_options, **job_params)
        self.tasks[tsk_kwargs["message_id"]] = job
        return job

    def run_task_right_now(self, job):
        task = BackgroundJobs.get_job_ref(job.task_name)
        task_id = str(uuid4())
        tsk_kwargs = {
            "on_success": jobs.success,
            "on_failure": jobs.failure,
            "kwargs": job.task_args,
            "message_id": task_id,
        }
        if job.meta_data:
            tsk_kwargs.update({**job.meta_data})
        job = self._scheduler.add_job(
            task.send_with_options,
            kwargs=tsk_kwargs,
            replace_existing=True,
            id=task_id,
        )
        self.tasks[task_id] = job
        return job

    def run_task(self, job: models.Job) -> Job:
        if job.task_type == ScheduleOptions.interval:
            return self.run_task_interval(job)
        if job.task_type == ScheduleOptions.cron:
            return self.run_task_cron(job)
        else:
            return self.run_task_right_now(job)

    @staticmethod
    def get_result(task_id):
        data = db.Hash(task_id)
        return deserialize(data["results"]) if "results" in data else []


jobber = BackgroundJobs()
