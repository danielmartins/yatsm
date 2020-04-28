from enum import Enum
from inspect import signature
from typing import Optional, Union

from apscheduler.triggers.cron import CronTrigger
from pydantic import BaseModel, root_validator, validator

from yatsm import jobs


class ScheduleOptions(str, Enum):
    no_schedule = "now"
    date = "date"
    interval = "interval"
    cron = "cron"


class IntervalOption(BaseModel):
    week: Optional[int]
    days: Optional[int]
    hours: Optional[int]
    minutes: Optional[int]
    seconds: Optional[int]
    start_date: Optional[str]
    end_date: Optional[str]
    jitter: Optional[int]


class CronOption(BaseModel):
    expression: str
    start_date: Optional[str]
    end_date: Optional[str]

    # @validator("expression")
    # def validate_cron_expression(cls, value, values, **kwargs):
    #     # Attempt to create from trigger, if fail raise ValueError
    #     CronTrigger.from_crontab(value)
    #     return value


class Job(BaseModel):
    task_name: str
    task_args: dict
    meta_data: dict = None
    task_type: ScheduleOptions = ScheduleOptions.no_schedule
    interval_options: Optional[IntervalOption]
    cron_options: Optional[CronOption]

    @root_validator()
    def valid_task_options(cls, values):
        if values["task_type"] == ScheduleOptions.interval:
            if not isinstance(values["interval_options"], IntervalOption):
                raise ValueError("Task type options dont match the task type option")
        if values["task_type"] == ScheduleOptions.cron:
            if not isinstance(values["cron_options"], CronOption):
                raise ValueError(
                    f"Task type options dont match the task type option {values['task_type']}"
                )
        return values

    @validator("task_name")
    def valid_task(cls, value):
        if value not in dir(jobs):
            raise ValueError("Unknown task")
        return value

    @validator("task_args")
    def valid_task_args(cls, value, values, **kwargs):
        task = getattr(jobs, values["task_name"])
        sign = signature(task.fn)
        for param in value.keys():
            print(param)
            if param not in sign.parameters:
                raise ValueError(f"Invalid job parameter [{param}]")
        return value


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    disabled: bool = None


class UserInDB(User):
    hashed_password: str
