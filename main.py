import sys
import schedule
import traceback
from datetime import datetime
from time import sleep
from general.clock_bot import ClockBot
from general.function import get_time_str
from general import WOKERS_INFO, SHIFT_INFO, FORM_URL, NAME_XPATH, SUBMIT_XPATH, SHIFT_N_ON_XPATH, SHIFT_N_OFF_XPATH, SHIFT_G_ON_XPATH, SHIFT_G_OFF_XPATH, SHIFT_M_ON_XPATH, SHIFT_M_OFF_XPATH, DRIVER_PATH
from general.clock_logger import logger, err_logger

def clock(shift_xpath, shift, on):
    try:
        for name, info in WOKERS_INFO.items():
            cb = ClockBot(FORM_URL, name, info['shift'], info['day_off'])
            cb.set_name_xpath(NAME_XPATH)
            cb.set_shift_type(shift)
            cb.set_shift_xpath(shift_xpath)
            cb.set_submit_xpath(SUBMIT_XPATH)
            cb.set_driver_path(DRIVER_PATH)
            cb.set_on(on)
            result = cb.run()
            if result:
                logger.info(f'{name} {info["shift"]} clock in')
            else:
                logger.info(f'{name} {info["shift"]} - {info["day_off"]} do noting')
    except Exception:
        logger.error(traceback.format_exc())
        err_logger.error(traceback.format_exc())

try:
    scheduler = schedule.Scheduler()
    scheduler.every().day.at(SHIFT_INFO['中班']['off']).do(
        clock,
        shift_xpath=SHIFT_N_OFF_XPATH,
        shift='中班',
        on=False
    )
    scheduler.every().day.at(SHIFT_INFO['早班']['on']).do(
        clock,
        shift_xpath=SHIFT_M_ON_XPATH,
        shift='早班',
        on=True
    )
    scheduler.every().day.at(SHIFT_INFO['晚班']['off']).do(
        clock,
        shift_xpath=SHIFT_G_OFF_XPATH,
        shift='晚班',
        on=False
    )
    scheduler.every().day.at(SHIFT_INFO['中班']['on']).do(
        clock,
        shift_xpath=SHIFT_N_ON_XPATH,
        shift='中班',
        on=True
    )
    scheduler.every().day.at(SHIFT_INFO['早班']['off']).do(
        clock,
        shift_xpath=SHIFT_M_OFF_XPATH,
        shift='早班',
        on=False
    )
    scheduler.every().day.at(SHIFT_INFO['晚班']['on']).do(
        clock,
        shift_xpath=SHIFT_G_ON_XPATH,
        shift='晚班',
        on=True
    )
except Exception:
    logger.error(traceback.format_exc())
    err_logger.error(traceback.format_exc())

if __name__ == '__main__':
    keep_sec = 0
    start_datetime = datetime.now().__format__('%Y-%m-%d %H:%M:%S')
    print(f'開始執行時間: {start_datetime}')
    while True:
        try:
            scheduler.run_pending()
            bar = f"\r已執行 {get_time_str(keep_sec)}"
            sys.stdout.write(bar)
            sys.stdout.flush()
        except Exception:
            logger.error(traceback.format_exc())
            err_logger.error(traceback.format_exc())
        keep_sec += 1
        sleep(1)
