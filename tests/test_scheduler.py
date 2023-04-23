import os
from pathlib import Path

from job import Job
from tests.conftest import TEST_NEW_DIR_PATH, TEST_NEW_FILE_PATH


class BaseTearDown:

    def teardown_method(self):
        """Remove logs and csv file."""
        log_file_path = os.path.join(Path(__file__).resolve().parent.parent, "logfile.log")
        test_file_path = TEST_NEW_FILE_PATH
        test_dir_path = TEST_NEW_DIR_PATH
        if os.path.exists(log_file_path):
            os.remove(log_file_path)
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
        if os.path.exists(test_dir_path):
            os.remove(test_dir_path)

class TestScheduler(BaseTearDown):

    def test_jobs_are_scheduled(self, scheduler, lambda_jobs):
        for job in lambda_jobs:
            scheduler.schedule(job)

        assert len(scheduler.pending_jobs) == len(lambda_jobs)

    def test_job_run_successful(self, scheduler, create_file_job):
        scheduler.schedule(create_file_job)
        scheduler.run()
        assert create_file_job in scheduler.completed_jobs
        assert os.path.exists(TEST_NEW_FILE_PATH)


    def test_failed_job(self, scheduler, job_with_exception):
        scheduler.schedule(job_with_exception)
        scheduler.run()
        assert job_with_exception in scheduler.failed_jobs


    def test_job_with_dependencies(self, scheduler, job_with_dependencies):
        scheduler.schedule(job_with_dependencies)
        scheduler.run()
        assert len(scheduler.completed_jobs) == 3


    def test_successful_timeout_job(self, scheduler, timeout_job):
        scheduler.schedule(timeout_job)
        scheduler.run()
        assert timeout_job in scheduler.completed_jobs

