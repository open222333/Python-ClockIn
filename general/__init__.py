from configparser import ConfigParser
from datetime import datetime
import os


config = ConfigParser()
config.read('config/config.ini', encoding='utf-8')

FORM_URL = config.get('INFO', 'FORM_URL', fallback='')
DRIVER_PATH = config.get('INFO', 'DRIVER_PATH', fallback='')
USER_SETTING_PATH = config.get('INFO', 'USER_SETTING_PATH', fallback='config/setting.json')
LOG_FILE_PATH = config.get('INFO', 'LOG_FILE_PATH', fallback=f'log/{datetime.now().__format__("%Y-%m-%d")}.log')
ERROR_LOG_FILE_PATH = config.get('INFO', 'ERROR_LOG_FILE_PATH', fallback=f'log/error-{datetime.now().__format__("%Y-%m-%d")}.log')

if not os.path.exists(os.path.dirname(LOG_FILE_PATH)):
    os.makedirs(os.path.dirname(LOG_FILE_PATH))

if not os.path.exists(LOG_FILE_PATH):
    with open(LOG_FILE_PATH, 'w') as f:
        pass

if not os.path.exists(os.path.dirname(ERROR_LOG_FILE_PATH)):
    os.makedirs(os.path.dirname(ERROR_LOG_FILE_PATH))

if not os.path.exists(ERROR_LOG_FILE_PATH):
    with open(ERROR_LOG_FILE_PATH, 'w') as f:
        pass

# XPATH
NAME_XPATH = config.get('XPATH', 'NAME_XPATH', fallback='')
SHIFT_M_ON_XPATH = config.get('XPATH', 'SHIFT_M_ON_XPATH', fallback='')
SHIFT_M_OFF_XPATH = config.get('XPATH', 'SHIFT_M_OFF_XPATH', fallback='')
SHIFT_N_ON_XPATH = config.get('XPATH', 'SHIFT_N_ON_XPATH', fallback='')
SHIFT_N_OFF_XPATH = config.get('XPATH', 'SHIFT_N_OFF_XPATH', fallback='')
SHIFT_G_ON_XPATH = config.get('XPATH', 'SHIFT_G_ON_XPATH', fallback='')
SHIFT_G_OFF_XPATH = config.get('XPATH', 'SHIFT_G_OFF_XPATH', fallback='')
SUBMIT_XPATH = config.get('XPATH', 'SUBMIT_XPATH', fallback='')
