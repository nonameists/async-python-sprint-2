from typing import Callable

from config import logger
from enums import JobStatuses


class Job:
    def __init__(self, func: Callable, start_at="", max_working_time=-1, tries=0, dependencies=None) -> None:
        self.func = func
        self.start_at = start_at
        self.max_working_time = max_working_time
        self.tries = tries
        self.dependencies = dependencies or []
        self.status = ""

    def run(self) -> None:
        """Public method tu run Job function."""
        while self.tries >= 0 and self.status != "stopped":
            try:
                logger.info(f"Start {self.func.__name__}")
                self.func()
                self.status = JobStatuses.COMPLETED
                logger.info(f"Function {self.func.__name__} successfully finished.")
            except Exception as error:
                logger.error(f"Function {self.func.__name__} failed with error {error}.")
                self.tries = -1
                # check if we need restart job function
                if self.tries < 0:
                    self.status = JobStatuses.FAILED
                    break
