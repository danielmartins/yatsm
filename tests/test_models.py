from assertpy import assert_that

from yatsm.models import CronOption, IntervalOption, Job, ScheduleOptions


def test_job_payload_model_cron():
    payload = {
        "task_name": "heavy_job",
        "task_args": {"url": "qweasd"},
        "meta_data": {},
        "task_type": "cron",
        "cron_options": {"expression": "* * * * *"},
    }

    j = Job(**payload)

    assert_that(j).is_instance_of(Job)
    assert_that(j.cron_options).is_instance_of(CronOption)
    assert_that(j.task_type).is_equal_to(ScheduleOptions.cron)


def test_job_payload_model_interval():
    payload = {
        "task_name": "heavy_job",
        "task_args": {"url": "qweasd"},
        "meta_data": {},
        "task_type": "interval",
        "interval_options": {"minutes": 1},
    }

    j = Job(**payload)

    assert_that(j).is_instance_of(Job)
    assert_that(j.interval_options).is_instance_of(IntervalOption)
    assert_that(j.task_type).is_equal_to(ScheduleOptions.interval)


def test_job_payload_model_now():
    payload = {
        "task_name": "heavy_job",
        "task_args": {"url": "qweasd"},
        "meta_data": {},
    }

    j = Job(**payload)

    assert_that(j).is_instance_of(Job)
    assert_that(j.task_type).is_equal_to(ScheduleOptions.no_schedule)
