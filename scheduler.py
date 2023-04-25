import pickle
from typing import List

from config import logger, PICKLE_DUMP_FILENAME
from enums import JobStatuses
from exceptions import PendingLimitException, JobTimeoutException
from executor import ExecutorService
from job import Job


class Scheduler:
    def __init__(self, pool_size: int = 10):
        self.pool_size = pool_size
        self.pending_jobs = []
        self.running_jobs = []
        self.failed_jobs = []
        self.completed_jobs = []
        self.executor = ExecutorService().execute()

    def schedule(self, job: Job) -> None:
        """Method for adding Job tasks to pending_tasks list."""
        try:
            self._add_task_to_pending_list(job)
            logger.info(f"Add Job {job.name} to pending list.")
        except PendingLimitException:
            logger.error(
                f"Can't add Job {job.name} to pending list. Pool size is exceeded."
            )

    def run(self) -> None:
        """Method runs job from pending jobs."""
        while self.pending_jobs:
            job = self.pending_jobs.pop()
            try:
                job.status = JobStatuses.RUNNING
                self.running_jobs.append(job)
                # check and run dependencies if exists
                if job.dependencies:
                    self._run_dependencies(job.dependencies)

                self.executor.send(job)
                self._relocate_job_if_complete(job)
            except JobTimeoutException as timeout_error:
                logger.error(
                    f"Exception: {timeout_error} occurred while running job: {job.name}"
                )
                self._relocate_job_if_fail(job)
            except Exception as error:
                logger.error(
                    f"Unexpected exception: {error} occurred while running job: {job.name}"
                )
                self._relocate_job_if_fail(job)

    def stop(self) -> None:
        """Method collect all pending + running tasks and serialize all tasks with pickle."""
        logger.info("Stop scheduler. Dump active jobs to a file.")
        all_tasks = self.pending_jobs + self.running_jobs
        try:
            with open(PICKLE_DUMP_FILENAME, "wb") as pickle_file:
                pickle.dump(all_tasks, pickle_file)
            logger.info(f"Successfully dump jobs to {PICKLE_DUMP_FILENAME}")
        except FileNotFoundError as file_not_found_error:
            logger.error(
                f"{file_not_found_error} occurred. Check path: {PICKLE_DUMP_FILENAME}"
            )
        except PermissionError as permission_error:
            logger.error(
                f"{permission_error} occurred. Check permission to a file: {PICKLE_DUMP_FILENAME}"
            )
        except Exception as error:
            logger.error(f"Occurred unexpected error: {error}")

    def restart(self) -> None:
        """Method load all tasks from pickle dump file and place them to pending tasks."""
        try:
            logger.info(
                f"Restart scheduler. Load jobs from a file: {PICKLE_DUMP_FILENAME}"
            )
            with open(PICKLE_DUMP_FILENAME, "rb") as pickle_dump_file:
                all_jobs = pickle.load(pickle_dump_file)

                # add previous pending jobs to pending list
                self.pending_jobs = [
                    job
                    for job in all_jobs
                    if job.status == JobStatuses.PENDING
                ]
                previous_running_jobs = [
                    job
                    for job in all_jobs
                    if job.status == JobStatuses.RUNNING
                ]

                # reset status from 'running' to 'pending
                for job in previous_running_jobs:
                    job.status = JobStatuses.PENDING
                    self.pending_jobs.append(job)

                # run all tasks again
                self.run()

        except FileNotFoundError as file_not_found_error:
            logger.error(
                f"{file_not_found_error} occurred. Check path: {PICKLE_DUMP_FILENAME}"
            )
        except PermissionError as permission_error:
            logger.error(
                f"{permission_error} occurred. Check permission to a file: {PICKLE_DUMP_FILENAME}"
            )
        except Exception as error:
            logger.error(f"Occurred unexpected error: {error}")

    def _add_task_to_pending_list(self, job: Job) -> None:
        """Private method try to add Job in pedning list."""
        if len(self.pending_jobs) < self.pool_size:
            job.status = JobStatuses.PENDING
            self.pending_jobs.append(job)
        else:
            raise PendingLimitException()

    def _run_dependencies(self, jobs_dependencies: List[Job]):
        """Private method run job dependencies and set job status, remove/add from job lists."""
        while jobs_dependencies:
            d_job = jobs_dependencies.pop()
            d_job.status = JobStatuses.RUNNING
            self.running_jobs.append(d_job)
            self.executor.send(d_job)

            d_job.status = JobStatuses.COMPLETED
            self.running_jobs.remove(d_job)
            self.completed_jobs.append(d_job)

    def _relocate_job_if_complete(self, job: Job) -> None:
        """Private method set 'completed' status to Job obj and relocate it to completed jobs."""
        job.status = JobStatuses.COMPLETED
        self.running_jobs.remove(job)
        self.completed_jobs.append(job)

    def _relocate_job_if_fail(self, job: Job) -> None:
        """Private method set 'failed' status to Job obj and relocate it to failed jobs."""
        self.running_jobs.remove(job)
        job.status = JobStatuses.FAILED
        self.failed_jobs.append(job)


