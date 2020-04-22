from assertpy import assert_that
from starlette.status import HTTP_200_OK

from yatsm.scheduler import submitted_jobs


def test_job_simple_creation_run_once_and_now(request_client):
    payload = {"task_name": "heavy_job", "task_args": {"url": "google.com"}}
    response = request_client.post("/job", json=payload)
    assert_that(response.status_code).is_equal_to(HTTP_200_OK)
    assert_that(response.json()).contains_key("job_id")
    assert_that(submitted_jobs, "Jobs submetidos para a execução").is_length(1)


def test_job_creation_with_scheduler(request_client):
    payload = {
        "task_name": "heavy_job",
        "task_args": {"url": "google.com.br"},
        "task_trigger": {
            "combine": "AND",
            "triggers": [
                {"name": "IntervalTrigger", "kwargs": {"hours": 2}},
                {"name": "CronTrigger", "kwargs": {"day_of_week": "sat,sun"}},
            ],
        },
        "task_metadata": {"when": "2020-04-21T16:00:43.119296-03:00"},
    }
    response = request_client.post("/job", json=payload)
    assert_that(response.status_code).is_equal_to(HTTP_200_OK)
    assert_that(response.json()).contains_key("job_id")
