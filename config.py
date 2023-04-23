import logging
import os
from pathlib import Path

logger_format = "%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

logging.basicConfig(
    filename="logfile.log",
    filemode="a",
    format=logger_format,
    level=logging.INFO
)

logger = logging.getLogger()

PICKLE_DUMP_FILENAME = "jobs.pickle"

DATE_TIME_FORMAT = "%d/%m/%Y %H:%M:%S"


NEW_DIR_PATH = os.path.join(Path(__file__).resolve().parent, "new_directory")
NEW_FILE_PATH = os.path.join(Path(__file__).resolve().parent, "new_file.txt")