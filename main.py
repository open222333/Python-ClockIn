import sys
import json
import schedule
import logging
import traceback
from datetime import datetime
from time import sleep
from general.clock_bot import ClockBot
from general.function import get_time_str
from general import USER_SETTING_PATH, FORM_URL, NAME_XPATH, SUBMIT_XPATH, SHIFT_N_ON_XPATH, SHIFT_N_OFF_XPATH, SHIFT_G_ON_XPATH, SHIFT_G_OFF_XPATH, SHIFT_M_ON_XPATH, SHIFT_M_OFF_XPATH, DRIVER_PATH, LOG_FILE_PATH, ERROR_LOG_FILE_PATH

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


def clock(shift_xpath, shift):
    try:
        with open(USER_SETTING_PATH, 'r') as f:
            workers = json.load(f)
        for name, info in workers.items():
            cb = ClockBot(FORM_URL, name, info['shift'], info['day_off'])
            cb.set_name_xpath(NAME_XPATH)
            cb.set_shift_type(shift)
            cb.set_shift_xpath(shift_xpath)
            cb.set_submit_xpath(SUBMIT_XPATH)
            cb.set_driver_path(DRIVER_PATH)
            result = cb.run()
            if result:
                logger.info(f'{name} {info["shift"]} 打卡')
            else:
                logger.warning(f'{name} {info["shift"]} 打卡失敗')
    except Exception as err:
        logger.error(err)


try:
    scheduler = schedule.Scheduler()
    scheduler.every().day.at("01:00").do(
        clock,
        shift_xpath=SHIFT_N_OFF_XPATH,
        shift='中班'
    )
    scheduler.every().day.at("07:40").do(
        clock,
        shift_xpath=SHIFT_M_ON_XPATH,
        shift='早班'
    )
    scheduler.every().day.at("09:00").do(
        clock,
        shift_xpath=SHIFT_G_OFF_XPATH,
        shift='晚班'
    )
    scheduler.every().day.at("15:40").do(
        clock,
        shift_xpath=SHIFT_N_ON_XPATH,
        shift='中班'
    )
    scheduler.every().day.at("17:00").do(
        clock,
        shift_xpath=SHIFT_M_OFF_XPATH,
        shift='早班'
    )
    scheduler.every().day.at("23:40").do(
        clock,
        shift_xpath=SHIFT_G_ON_XPATH,
        shift='晚班'
    )
except Exception as err:
    logger.error(err)

if __name__ == '__main__':
    keep_sec = 0
    start_datetime = datetime.now().__format__('%Y-%m-%d %H:%M:%S')
    print(f'開始執行時間: {start_datetime}')
    while True:
        try:
            schedule.run_pending()
            bar = f"\r已執行 {get_time_str(keep_sec)}"
            sys.stdout.write(bar)
            sys.stdout.flush()
        except Exception as err:
            logger.error(traceback.format_exc())
        keep_sec += 1
        sleep(1)
