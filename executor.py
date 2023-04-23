import time
from datetime import datetime
from multiprocessing import Process
from threading import Timer
from typing import Generator

from config import logger
from exceptions import JobTimeoutException
from utils import coroutine


class ExecutorService:
    @coroutine
    def execute(self):
        """Method receive job object and run it."""
        while True:
            # receive job object
            job = yield
            # check if we need to start job function with delay
            if job.start_at > datetime.now().timestamp():
                delay_executor = self._execute_with_delay()
                delay_executor.send(job)
            elif job.max_working_time > 0:
                max_working_time_executor = self._execute_with_max_working_time()
                max_working_time_executor.send(job)
            else:
                job.run()

    @coroutine
    def _execute_with_delay(self) -> Generator:
        """Method receive job with delay."""
        while True:
            delayed_job = yield
            time_thread = Timer(interval=delayed_job.start_at.timestamp() - time.time(), function=delayed_job.run)
            time_thread.start()
            time_thread.join()

    @coroutine
    def _execute_with_max_working_time(self) -> Generator:
        """Method receive job with maximum working time."""
        while True:
            max_time_job = yield
            max_time_process = Process(target=max_time_job.run)
            max_time_process.start()
            max_time_process.join(timeout=max_time_job.max_working_time)

            if max_time_process.is_alive():
                max_time_process.terminate()
                logger.error(f"Job: {max_time_process.name} was terminated because of timeout.")
                raise JobTimeoutException()
