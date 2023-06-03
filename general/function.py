from . import TELEGRAM_API_KEY, TELEGRAM_CHAT_ID, CREATE_CHAT_ID
from . import logger

from datetime import datetime, timedelta
from random import randint
from typing import Union
import requests
import os


def get_time_str(total_secends: Union[int, float]) -> str:
    """依照秒數 回傳中文時間

    Args:
        total_secends (int): 總秒數

    Returns:
        str: 回傳時間
    """
    msg = ''
    seconds = total_secends % 60
    minutes = (total_secends // 60) % 60
    hours = ((total_secends // 60) // 60) % 24
    days = ((total_secends // 60) // 60) // 24
    if days != 0:
        msg += f"{int(days)}天"
    if hours != 0:
        msg += f"{int(hours)}時"
    if minutes != 0:
        msg += f"{int(minutes)}分"
    if seconds != 0:
        msg += f"{int(round(seconds, 0))}秒"
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


def get_file_extension(file_path: str) -> str:
    """取得 副檔名

    Args:
        file_path (str): 檔案路徑

    Returns:
        str: 副檔名
    """
    _, extension = os.path.splitext(file_path)  # 路徑 以及副檔名
    return extension


def send_message(message: str):
    """發送訊息到TG

    Args:
        message (str): 訊息內容
    """
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
