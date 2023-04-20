import logging

logger_format = "%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

logging.basicConfig(
    filename="logfile.log",
    filemode="a",
    format=logger_format,
    level=logging.INFO
)

logger = logging.getLogger()

PICKLE_DUMP_FILENAME = "jobs.pickle"
