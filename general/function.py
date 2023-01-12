from . import LOG_DIR_PATH, REMOVE_LOG_DAYS
from .clock_logger import logger
from datetime import datetime, timedelta
from random import randint
from traceback import format_exc
import os


def get_time_str(total_secends: int) -> str:
    '''依照秒數 回傳時間'''
    msg = ''
    seconds = total_secends % 60
    minutes = (total_secends // 60) % 60
    hours = ((total_secends // 60) // 60) % 24
    days = ((total_secends // 60) // 60) // 24
    if days != 0:
        msg += f"{str(days).center(3)}天"
    if hours != 0:
        msg += f"{str(hours).center(2)}時"
    if minutes != 0:
        msg += f"{str(minutes).center(2)}分"
    if seconds != 0:
        msg += f"{str(seconds).center(2)}秒"
    return msg


def random_time(time_s: str, max_minute: int, min_minute: int = 0) -> str:
    """回傳隨機時間

    Args:
        time_s (str): 時間字串 格式為"00:00"
        max_minute (int): 最大隨機整數
        min_minute (int, optional): 最小隨機整數. Defaults to 0.

    Returns:
        str: 回傳時間字串格式 "00:00"
    """
    struct_t = datetime.strptime(time_s, "%H:%M")
    return (struct_t + timedelta(minutes=randint(min_minute, max_minute))).strftime("%H:%M")


def is_overdue(file_path: str, day: int) -> bool:
    """檢查 檔案創建時間是否超過指定天數

    Args:
        file_path (str): 檔案路徑
        day (int): 指定天數

    Returns:
        bool: _description_
    """
    nt = datetime.now().date()
    ct = datetime.utcfromtimestamp(os.path.getctime(file_path)).date()
    return (nt - ct).days > day


def get_log_file(log_dir_path: str):
    log_files = []
    for file in os.listdir(log_dir_path):
        if get_file_extension(file) == '.log':
            log_files.append(f"{os.path.abspath(log_dir_path)}/{file}")
    return log_files


def get_file_extension(file_path):
    '''取得 副檔名'''
    _, extension = os.path.splitext(file_path)  # 路徑 以及副檔名
    return extension


def remove_file(file_path: str):
    os.remove(file_path)


def check_logs():
    try:
        for log_path in get_log_file(LOG_DIR_PATH):
            if is_overdue(log_path, REMOVE_LOG_DAYS):
                remove_file(log_path)
    except:
        logger.error(format_exc())
