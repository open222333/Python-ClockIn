
from . import LOG_FILE_PATH, ERROR_LOG_FILE_PATH, SCHEDULE_LOG_FILE_PATH, DEBUG
import logging


logger = logging.getLogger('main')
err_logger = logging.getLogger('main_error')
schedule_logger = logging.getLogger('schedule')
schedule_logger.propagate = False

if DEBUG:
    logger.setLevel(logging.DEBUG)
    schedule_logger.setLevel(logging.DEBUG)

log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

log_handler = logging.FileHandler(LOG_FILE_PATH)
err_log_handler = logging.FileHandler(ERROR_LOG_FILE_PATH)
schedule_log_handler = logging.FileHandler(SCHEDULE_LOG_FILE_PATH)

log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)

err_log_handler.setFormatter(log_formatter)
err_logger.addHandler(err_log_handler)

schedule_log_handler.setFormatter(log_formatter)
schedule_logger.addHandler(schedule_log_handler)
