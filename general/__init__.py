import re
import os
import sys
import json
import socket
import requests
import logging
from traceback import print_exc
from configparser import ConfigParser
from bs4 import BeautifulSoup
from .clock_logger import Log


config = ConfigParser()
if sys.platform == 'linux' or sys.platform == 'darwin':
    # macOS : darwin
    # Linux : linux
    config.read('config/config.ini', encoding='utf-8')

    USER_SETTING_PATH = config.get('INFO', 'USER_SETTING_PATH', fallback='config/setting.json')
    SHIFT_JSON_FILE_PATH = config.get('INFO', 'SHIFT_JSON_FILE_PATH', fallback='config/shift.json')
elif sys.platform == 'win32':
    # Windows
    config.read('config\config.ini', encoding='utf-8')

    USER_SETTING_PATH = config.get('INFO', 'USER_SETTING_PATH', fallback='config\setting.json')
    SHIFT_JSON_FILE_PATH = config.get('INFO', 'SHIFT_JSON_FILE_PATH', fallback='config\shift.json')

# log設定
try:
    HOSTNAME = socket.gethostname()

    LOG_PATH = config.get('INFO', 'LOG_PATH', fallback='logs')

    # 關閉log
    LOG_DISABLE = config.getboolean('INFO', 'LOG_DISABLE', fallback=False)

    # 關閉記錄檔案
    LOG_FILE_DISABLE = config.getboolean('INFO', 'LOG_FILE_DISABLE', fallback=False)

    # 設定紀錄log等級 預設WARNING, DEBUG,INFO,WARNING,ERROR,CRITICAL
    LOG_LEVEL = config.get('INFO', 'LOG_LEVEL', fallback='WARNING')

    # 指定log大小(輸入數字) 單位byte
    LOG_SIZE = config.getint('INFO', 'LOG_SIZE', fallback=0)
    # 指定保留log天數(輸入數字) 預設7
    LOG_DAYS = config.getint('INFO', 'LOG_DAYS', fallback=7)

    log_setting = {
        'HOSTNAME': HOSTNAME,
        'LOG_PATH': LOG_PATH,
        'LOG_DISABLE': LOG_DISABLE,
        'LOG_FILE_DISABLE': LOG_FILE_DISABLE,
        'LOG_LEVEL': LOG_LEVEL,
        'LOG_SIZE': LOG_SIZE,
        'LOG_DAYS': LOG_DAYS
    }
except Exception as err:
    print_exc()

# 建立log資料夾
if not os.path.exists(LOG_PATH) and not LOG_DISABLE:
    os.makedirs(LOG_PATH)

if LOG_DISABLE:
    logging.disable()

logger = Log()
if not LOG_FILE_DISABLE:
    logger.set_date_handler()
logger.set_msg_handler()
if LOG_LEVEL:
    logger.set_level(LOG_LEVEL)

err_logger = Log('error')
if not LOG_FILE_DISABLE:
    err_logger.set_date_handler()
err_logger.set_msg_handler()

USE_SELENIUM = config.getboolean('INFO', 'USE_SELENIUM', fallback=False)
FORM_URL = config.get('INFO', 'FORM_URL', fallback='')

# 隨機時間範圍
try:
    MAX_MINUTE = config.getint('RANDOM', 'MAX_MINUTE', fallback=0)
    MIN_MINUTE = config.getint('RANDOM', 'MIN_MINUTE', fallback=0)
except Exception as err:
    err_logger.error(err, exc_info=True)

# SELENIUM_INFO
DRIVER_PATH = config.get('SELENIUM_INFO', 'DRIVER_PATH', fallback='')
NAME_XPATH = config.get(
    'SELENIUM_INFO', 'NAME_XPATH',
    fallback='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
SHIFT_M_ON_XPATH = config.get(
    'SELENIUM_INFO', 'SHIFT_M_ON_XPATH',
    fallback='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[2]/label[1]/div/div')
SHIFT_M_OFF_XPATH = config.get(
    'SELENIUM_INFO', 'SHIFT_M_OFF_XPATH',
    fallback='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[4]/label[1]/div/div')
SHIFT_N_ON_XPATH = config.get(
    'SELENIUM_INFO', 'SHIFT_N_ON_XPATH',
    fallback='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[2]/label[2]/div/div')
SHIFT_N_OFF_XPATH = config.get(
    'SELENIUM_INFO', 'SHIFT_N_OFF_XPATH',
    fallback='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[4]/label[2]/div/div')
SHIFT_G_ON_XPATH = config.get(
    'SELENIUM_INFO', 'SHIFT_G_ON_XPATH',
    fallback='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[2]/label[3]/div/div')
SHIFT_G_OFF_XPATH = config.get(
    'SELENIUM_INFO', 'SHIFT_G_OFF_XPATH',
    fallback='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[4]/label[3]/div/div')
SUBMIT_XPATH = config.get(
    'SELENIUM_INFO', 'SUBMIT_XPATH',
    fallback='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span')

# 排班資訊
try:
    with open(SHIFT_JSON_FILE_PATH, 'r', encoding='utf-8') as f:
        SHIFT_INFO = json.load(f)

    with open(USER_SETTING_PATH, 'r', encoding='utf-8') as f:
        WOKERS_INFO = json.load(f)

except Exception as err:
    err_logger.error(err, exc_info=True)

# REQUESTS_INFO
SELECTOR_POST_URL = config.get('REQUESTS_INFO', 'SELECTOR_POST_URL', fallback='')
SELECTOR_NAME_COLUMN = config.get('REQUESTS_INFO', 'SELECTOR_NAME_COLUMN', fallback='')
SELECTOR_CLOCK_IN = config.get('REQUESTS_INFO', 'SELECTOR_CLOCK_IN', fallback='')
SELECTOR_CLOCK_OFF = config.get('REQUESTS_INFO', 'SELECTOR_CLOCK_OFF', fallback='')

# 表單資訊
try:
    res = requests.get(FORM_URL)
    soup = BeautifulSoup(res.text, 'lxml')

    # REQUESTS_INFO
    MORNING_MSG = config.get('REQUESTS_INFO', 'MORNING_MSG', fallback='早班08:00~17:00')
    NIGHT_MSG = config.get('REQUESTS_INFO', 'NIGHT_MSG', fallback='中班16:00~01:00')
    GRAVEYARD_MSG = config.get('REQUESTS_INFO', 'GRAVEYARD_MSG', fallback='晚班00:00~09:00')

    # 上班 選取格ID selector
    if SELECTOR_CLOCK_IN == '':
        SELECTOR_CLOCK_IN = "#mG61Hd > div > div > div > div:nth-child(2) > div > div > div > div > div > div > div:nth-child(2) > label > div > div"

    # 下班 選取格ID selector
    if SELECTOR_CLOCK_OFF == '':
        SELECTOR_CLOCK_OFF = "#mG61Hd > div > div > div > div:nth-child(2) > div > div > div > div > div > div > div:nth-child(4) > label > div > div"

    # 取得 填寫名稱ID selector
    if SELECTOR_NAME_COLUMN == '':
        SELECTOR_NAME_COLUMN = "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(1) > div"

    POST_URL = soup.select_one("#mG61Hd").attrs['action']

    CHECK_BOX_ID = {}
    for i in soup.select(SELECTOR_CLOCK_IN):
        if i.attrs['data-field-id'] not in CHECK_BOX_ID:
            CHECK_BOX_ID['on'] = i.attrs['data-field-id']
    for i in soup.select(SELECTOR_CLOCK_OFF):
        if i.attrs['data-field-id'] not in CHECK_BOX_ID:
            CHECK_BOX_ID['off'] = i.attrs['data-field-id']

    NAME_COLUMN_ID = re.findall(r'[\d]{0,20}', soup.select_one(SELECTOR_NAME_COLUMN).attrs['data-params'].split('[')[3])[0]
except Exception as err:
    err_logger.error(err, exc_info=True)


# Telegram Bot 的 API 金鑰
TELEGRAM_API_KEY = config.get('TELEGRAM', 'TELEGRAM_API_KEY', fallback=None)

# Telegram 使用者的 Chat ID
CREATE_CHAT_ID = None
if TELEGRAM_API_KEY:
    response = requests.get(f'https://api.telegram.org/bot{TELEGRAM_API_KEY}/getUpdates')
    data = response.json()
    CREATE_CHAT_ID = data['result'][0]['message']['chat']['id']

TELEGRAM_CHAT_ID = config.get('TELEGRAM', 'TELEGRAM_CHAT_ID', fallback=CREATE_CHAT_ID)
