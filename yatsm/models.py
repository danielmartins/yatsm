from inspect import signature

from pydantic import BaseModel, validator

from yatsm import jobs


class Job(BaseModel):
    task_name: str
    task_args: dict
    meta_data: dict = None

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