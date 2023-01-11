from datetime import datetime, timedelta
from random import randint


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
