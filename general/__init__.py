from configparser import ConfigParser
from datetime import datetime
from bs4 import BeautifulSoup
import os
import sys
import json
import traceback
import requests
import logging


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


FORM_URL = config.get('INFO', 'FORM_URL', fallback='')
USE_SELENIUM = bool(int(config.get('INFO', 'USE_SELENIUM', fallback=0)))
DRIVER_PATH = config.get('INFO', 'DRIVER_PATH', fallback='')

DEBUG = bool(int(config.get('INFO', 'DEBUG', fallback=0)))

LOG_FILE_NAME = config.get('INFO', 'LOG_FILE_NAME', fallback=f'{datetime.now().__format__("%Y-%m-%d")}.log')
ERROR_LOG_FILE_NAME = config.get('INFO', 'ERROR_LOG_FILE_NAME', fallback=f'error-{datetime.now().__format__("%Y-%m-%d")}.log')
SCHEDULE_LOG_FILE_NAME = config.get('INFO', 'SCHEDULE_LOG_FILE_NAME', fallback=f'schedule-{datetime.now().__format__("%Y-%m-%d")}.log')

LOG_DIR_PATH = config.get('INFO', 'LOG_DIR_PATH', fallback='log')
REMOVE_LOG_DAYS = int(config.get('INFO', 'LOG_DIR_PATH', fallback=7))

if sys.platform == 'linux' or sys.platform == 'darwin':
    # macOS : darwin
    # Linux : linux
    LOG_FILE_PATH = f"{LOG_DIR_PATH}/{LOG_FILE_NAME}"
    ERROR_LOG_FILE_PATH = f"{LOG_DIR_PATH}/{ERROR_LOG_FILE_NAME}"
    SCHEDULE_LOG_FILE_PATH = f"{LOG_DIR_PATH}/{SCHEDULE_LOG_FILE_NAME}"
elif sys.platform == 'win32':
    # Windows
    LOG_FILE_PATH = f"{LOG_DIR_PATH}\{LOG_FILE_NAME}"
    ERROR_LOG_FILE_PATH = f"{LOG_DIR_PATH}\{ERROR_LOG_FILE_NAME}"
    SCHEDULE_LOG_FILE_PATH = f"{LOG_DIR_PATH}\{SCHEDULE_LOG_FILE_NAME}"


init_logger = logging.getLogger('init')
init_log_handler = logging.FileHandler(ERROR_LOG_FILE_PATH)
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
init_log_handler.setFormatter(log_formatter)
init_logger.addHandler(init_log_handler)

try:
    if not os.path.exists(LOG_DIR_PATH):
        os.makedirs(LOG_DIR_PATH)

    if not os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, 'w') as f:
            pass

    if not os.path.exists(ERROR_LOG_FILE_PATH):
        with open(ERROR_LOG_FILE_PATH, 'w') as f:
            pass

    if not os.path.exists(SCHEDULE_LOG_FILE_PATH):
        with open(SCHEDULE_LOG_FILE_PATH, 'w') as f:
            pass
except Exception:
    init_logger.error(traceback.format_exc())


# 隨機時間範圍
try:
    MAX_MINUTE = int(config.get('RANDOM', 'MAX_MINUTE', fallback=0))
    MIN_MINUTE = int(config.get('RANDOM', 'MIN_MINUTE', fallback=0))
except Exception:
    init_logger.error(traceback.format_exc())

# XPATH
NAME_XPATH = config.get('XPATH', 'NAME_XPATH', fallback='')
SHIFT_M_ON_XPATH = config.get('XPATH', 'SHIFT_M_ON_XPATH', fallback='')
SHIFT_M_OFF_XPATH = config.get('XPATH', 'SHIFT_M_OFF_XPATH', fallback='')
SHIFT_N_ON_XPATH = config.get('XPATH', 'SHIFT_N_ON_XPATH', fallback='')
SHIFT_N_OFF_XPATH = config.get('XPATH', 'SHIFT_N_OFF_XPATH', fallback='')
SHIFT_G_ON_XPATH = config.get('XPATH', 'SHIFT_G_ON_XPATH', fallback='')
SHIFT_G_OFF_XPATH = config.get('XPATH', 'SHIFT_G_OFF_XPATH', fallback='')
SUBMIT_XPATH = config.get('XPATH', 'SUBMIT_XPATH', fallback='')

# 排班資訊
try:
    with open(SHIFT_JSON_FILE_PATH, 'r', encoding='utf-8') as f:
        SHIFT_INFO = json.load(f)

    with open(USER_SETTING_PATH, 'r', encoding='utf-8') as f:
        WOKERS_INFO = json.load(f)

except Exception:
    init_logger.error(traceback.format_exc())

NAME_COLUMN_ID = config.get('SELECTOR', 'NAME_COLUMN_ID', fallback='')

SELECTOR_POST_URL = config.get('SELECTOR', 'SELECTOR_POST_URL', fallback='')
SELECTOR_CLOCK_IN = config.get('SELECTOR', 'SELECTOR_CLOCK_IN', fallback='')
SELECTOR_CLOCK_OFF = config.get('SELECTOR', 'SELECTOR_CLOCK_OFF', fallback='')

# 表單資訊
try:
    res = requests.get(FORM_URL)
    soup = BeautifulSoup(res.text, 'lxml')

    MORNING_MSG = config.get('SELECTOR', 'MORNING_MSG', fallback='早班08:00~17:00')
    NIGHT_MSG = config.get('SELECTOR', 'NIGHT_MSG', fallback='中班16:00~01:00')
    GRAVEYARD_MSG = config.get('SELECTOR', 'NIGHT_MSG', fallback='晚班00:00~09:00')

    # 上班
    if SELECTOR_CLOCK_IN == '':
        SELECTOR_CLOCK_IN = "#mG61Hd > div > div > div > div:nth-child(2) > div > div > div > div > div > div > div:nth-child(2) > label > div > div"

    # 下班
    if SELECTOR_CLOCK_OFF == '':
        SELECTOR_CLOCK_OFF = "#mG61Hd > div > div > div > div:nth-child(2) > div > div > div > div > div > div > div:nth-child(4) > label > div > div"

    POST_URL = soup.select_one("#mG61Hd").attrs['action']

    CHECK_BOX_ID = {}
    for i in soup.select(SELECTOR_CLOCK_IN):
        if i.attrs['data-field-id'] not in CHECK_BOX_ID:
            CHECK_BOX_ID['on'] = i.attrs['data-field-id']
        # CHECK_BOX_ID[i.attrs['data-field-id']].append(i.attrs['data-answer-value'])
    for i in soup.select(SELECTOR_CLOCK_OFF):
        if i.attrs['data-field-id'] not in CHECK_BOX_ID:
            CHECK_BOX_ID['off'] = i.attrs['data-field-id']
        # CHECK_BOX_ID[i.attrs['data-field-id']].append(i.attrs['data-answer-value'])
except Exception:
    init_logger.error(traceback.format_exc())
