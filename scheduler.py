import pickle

from config import logger, PICKLE_DUMP_FILENAME
from enums import JobStatuses
from exceptions import PendingLimitException, JobTimeoutException
from executor import ExecutorService
from job import Job


class Scheduler:
    def __init__(self, pool_size=10):
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
            logger.error(f"Can't add Job {job.name} to pending list. Pool size is exceeded.")

    def run(self):
        while self.pending_jobs:
            job = self.pending_jobs.pop()
            try:
                job.status = JobStatuses.RUNNING
                self.running_jobs.append(job)
                if job.dependencies:
                    for d_job in job.dependencies:
                        d_job.status = JobStatuses.RUNNING
                        self.executor.send(d_job)
                else:
                    self.executor.send(job)
                job.status = JobStatuses.COMPLETED
                self.running_jobs.remove(job)
                self.completed_jobs.append(job)
            except (JobTimeoutException, Exception) as error:
                logger.error(f"Exception: {error} occurred while running job: {job.name}")
                self.running_jobs.remove(job)
                job.status = JobStatuses.FAILED
                self.failed_jobs.append(job)

    def stop(self) -> None:
        """Method collect all pending + running tasks and serialize all tasks with pickle."""
        all_tasks = self.pending_jobs + self.running_jobs
        with open(PICKLE_DUMP_FILENAME, "wb") as pickle_file:
            pickle.dump(all_tasks, pickle_file)

    def restart(self) -> None:
        """Method load all tasks from pickle dump file and place them to pending tasks."""
        with open(PICKLE_DUMP_FILENAME, "rb") as pickle_dump_file:
            all_jobs = pickle.load(pickle_dump_file)

        # add previous pending jobs to pending list
        self.pending_jobs = [job for job in all_jobs if job.status == JobStatuses.PENDING]
        previous_running_jobs = [job for job in all_jobs if job.status == JobStatuses.RUNNING]

        # reset status from 'running' to 'pending
        for job in previous_running_jobs:
            job.status = JobStatuses.PENDING
            self.pending_jobs.append(job)

        # run all tasks again
        self.run()

    def _add_task_to_pending_list(self, job: Job) -> None:
        """Private method try to add Job in pedning list."""
        if len(self.pending_jobs) < self.pool_size:
            job.status = JobStatuses.PENDING
            self.pending_jobs.append(job)
        else:
            raise PendingLimitException()

