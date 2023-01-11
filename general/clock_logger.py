
from . import LOG_FILE_PATH, ERROR_LOG_FILE_PATH
import logging


logger = logging.getLogger('clock_bot')
logger.setLevel(logging.DEBUG)

err_logger = logging.getLogger('clock_bot_error')

log_handler = logging.FileHandler(LOG_FILE_PATH)
err_log_handler = logging.FileHandler(ERROR_LOG_FILE_PATH)
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)

err_log_handler.setFormatter(log_formatter)
err_logger.addHandler(err_log_handler)
