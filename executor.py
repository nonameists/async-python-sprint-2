import time
from datetime import datetime
from threading import Timer, Thread

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
                thread = Timer(interval=job.start_at.timestamp() - time.time(), function=job.run)
            else:
                thread = Thread(target=job.run)
            thread.start()
