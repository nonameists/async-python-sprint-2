import pickle

from config import logger, PICKLE_DUMP_FILENAME
from enums import JobStatuses
from exceptions import PendingLimitException
from executor import ExecutorService
from job import Job


class Scheduler:
    def __init__(self, pool_size=10):
        self.pool_size = pool_size
        self.pending_tasks = []
        self.running_tasks = []
        self.failed_tasks = []
        self.completed_tasks = []
        self.executor_service = ExecutorService()

    def schedule(self, job: Job) -> None:
        """Method for adding Job tasks to pending_tasks list."""
        try:
            self._add_task_to_pending_list(job)
            logger.info(f"Add Job {job.name} to pending list.")
        except PendingLimitException:
            logger.error(f"Can't add Job {job.name} to pending list. Pool size is exceeded.")


    def run(self):
        pass

    def stop(self) -> None:
        """Method collect all pending + running tasks and serialize all tasks with pickle."""
        all_tasks = self.pending_tasks + self.running_tasks
        with open(PICKLE_DUMP_FILENAME, "wb") as pickle_file:
            pickle.dump(all_tasks, pickle_file)

    def restart(self) -> None:
        """Method load all tasks from pickle dump file and place them to pending tasks."""
        with open(PICKLE_DUMP_FILENAME, "rb") as pickle_dump_file:
            all_tasks = pickle.load(pickle_dump_file)

        # add previous pending jobs to pending list
        self.pending_tasks = [job for job in all_tasks if job.status == JobStatuses.PENDING]
        previous_running_tasks = [job for job in all_tasks if job.status == JobStatuses.RUNNING]

        # reset status from 'running' to 'pending
        for job in previous_running_tasks:
            job.status = JobStatuses.PENDING
            self.pending_tasks.append(job)

        # run all tasks again
        self.run()

    def _add_task_to_pending_list(self, job: Job) -> None:
        """Private method try to add Job in pedning list."""
        if len(self.pending_tasks) < self.pool_size:
            job.status = JobStatuses.PENDING
            self.pending_tasks.append(job)
        else:
            raise PendingLimitException()

