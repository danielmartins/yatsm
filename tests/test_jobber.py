from apscheduler.triggers.combining import AndTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from assertpy import assert_that

from yatsm.jobber import trigger_factory


def test_job_trigger_composer():
    trigger = {
        "combine": "AND",
        "triggers": [
            {"name": "IntervalTrigger", "kwargs": {"hours": 2}},
            {"name": "CronTrigger", "kwargs": {"day_of_week": "sat,sun"}},
        ],
    }
    parsed_trigger = trigger_factory(trigger)
    assert_that(parsed_trigger).is_instance_of(AndTrigger)
    assert_that(parsed_trigger.triggers).is_length(2)
    assert_that(parsed_trigger.triggers[0]).is_instance_of(IntervalTrigger)
    assert_that(parsed_trigger.triggers[1]).is_instance_of(CronTrigger)
