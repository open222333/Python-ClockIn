from datetime import datetime, timedelta
from . import TELEGRAM_API_KEY, TELEGRAM_CHAT_ID, CREATE_CHAT_ID
import requests
from random import randint
from . import logger
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
    logger.debug(f'is_overdue\n{file_path}\n現在時間: {nt} 檔案建立時間: {ct}')
    return (nt - ct).days > day


def get_file_extension(file_path):
    '''取得 副檔名'''
    _, extension = os.path.splitext(file_path)  # 路徑 以及副檔名
    return extension


def send_message(message: str):
    if TELEGRAM_API_KEY:
        url = f'https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage'
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message
        }
        response = requests.post(url, data=data)
        if response.status_code != 200:
            logger.error(f'無法發送訊息至 Telegram:\n{response.json()}')
            data = {
                'chat_id': CREATE_CHAT_ID,
                'text': f'無法發送訊息至 Telegram:\n{response.json()}'
            }
            requests.post(url, data=data)
