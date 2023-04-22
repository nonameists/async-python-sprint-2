from datetime import datetime
from typing import Callable, Optional

from config import logger, DATE_TIME_FORMAT
from enums import JobStatuses


class Job:
    def __init__(
            self, name: str, func: Callable,
            start_at: Optional[str] = None,
            max_working_time=-1, tries=0, dependencies=None
    ) -> None:
        self.name = name
        self.func = func
        self.start_at = self._convert_to_datetime(start_at)
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

    def _convert_to_datetime(self, date: Optional[str]) -> Optional[float]:
        if date is None:
            return None
        try:
            return datetime.strptime(date, DATE_TIME_FORMAT).timestamp()
        except ValueError:
            logger.error(f"Receive unsupported date format% {date}. Date_time format should be: {DATE_TIME_FORMAT}")
            return None
