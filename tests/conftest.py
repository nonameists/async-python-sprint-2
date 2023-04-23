import os
import time
from pathlib import Path

import pytest

from job import Job
from scheduler import Scheduler
from tasks import hello_world, hello_world_2, hello_world_3

TEST_NEW_DIR_PATH = os.path.join(Path(__file__).resolve().parent, "test_new_directory")
TEST_NEW_FILE_PATH = os.path.join(Path(__file__).resolve().parent, "test_new_file.txt")


@pytest.fixture()
def scheduler():
    return Scheduler()


@pytest.fixture()
def job_with_dependencies():
    job_dependencies = [
        Job(name="hello_world_2_task", func=hello_world_2),
        Job(name="hello_world_3_task", func=hello_world_3)
    ]
    return Job(name="hello_world_task", func=hello_world, dependencies=job_dependencies)


@pytest.fixture()
def timeout_job():
    return Job(name="big_timeout_task", func=timeout_func, max_working_time=1)


@pytest.fixture()
def lambda_jobs():
    return [
        Job(name="Test lambda_1 job", func=lambda: "hello job_1!"),
        Job(name="Test lambda_2 job", func=lambda: "hello job_2!")
    ]

@pytest.fixture()
def job_with_exception():
    return Job(name="job with exception", func=error_func)


def timeout_func():
    time.sleep(0.3)


def error_func():
    raise Exception('AAAAAAA')
