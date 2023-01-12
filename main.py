import sys
import schedule
import traceback
from random import randint
from datetime import datetime
from time import sleep
from general.clock_bot import ClockBot
from general.function import get_time_str, check_logs
from general import WOKERS_INFO, SHIFT_INFO, FORM_URL, NAME_XPATH, SUBMIT_XPATH, SHIFT_N_ON_XPATH, SHIFT_N_OFF_XPATH, SHIFT_G_ON_XPATH, SHIFT_G_OFF_XPATH, SHIFT_M_ON_XPATH, SHIFT_M_OFF_XPATH, DRIVER_PATH, USE_SELENIUM, POST_URL, CHECK_BOX_ID, NAME_COLUMN_ID, MORNING_MSG, NIGHT_MSG, GRAVEYARD_MSG, MAX_MINUTE, MIN_MINUTE
from general.clock_logger import logger, err_logger


def clock(shift_xpath, shift, on, msg):
    try:
        for name, info in WOKERS_INFO.items():
            s = '上班' if on else '下班'
            logger.info(f'{name} {shift} {s}')
            cb = ClockBot(FORM_URL, name, info['shift'], info['day_off'])
            if USE_SELENIUM:
                cb.set_selenium()
                cb.set_name_xpath(NAME_XPATH)
                cb.set_shift_xpath(shift_xpath)
                cb.set_submit_xpath(SUBMIT_XPATH)
                cb.set_driver_path(DRIVER_PATH)
            else:
                cb.set_requests_info(
                    post_url=POST_URL,
                    name_id=NAME_COLUMN_ID,
                    on_id=CHECK_BOX_ID['on'],
                    off_id=CHECK_BOX_ID['off'],
                    check_box_value=msg
                )
            # 設置隨機時間
            cb.set_sleep_sec(randint(MIN_MINUTE, MAX_MINUTE))
            # 設置班別
            cb.set_shift_type(shift)
            # 設置上下班
            cb.set_duty(on)
            cb.run()
    except Exception:
        logger.error(traceback.format_exc())
        err_logger.error(traceback.format_exc())

try:
    scheduler = schedule.Scheduler()
    scheduler.every().day.at(SHIFT_INFO['早班']['on']).do(
        clock,
        shift_xpath=SHIFT_M_ON_XPATH,
        shift='早班',
        on=True,
        msg=MORNING_MSG
    )
    scheduler.every().day.at(SHIFT_INFO['早班']['off']).do(
        clock,
        shift_xpath=SHIFT_M_OFF_XPATH,
        shift='早班',
        on=False,
        msg=MORNING_MSG
    )
    scheduler.every().day.at(SHIFT_INFO['中班']['on']).do(
        clock,
        shift_xpath=SHIFT_N_ON_XPATH,
        shift='中班',
        on=True,
        msg=NIGHT_MSG
    )
    scheduler.every().day.at(SHIFT_INFO['中班']['off']).do(
        clock,
        shift_xpath=SHIFT_N_OFF_XPATH,
        shift='中班',
        on=False,
        msg=NIGHT_MSG
    )
    scheduler.every().day.at(SHIFT_INFO['晚班']['on']).do(
        clock,
        shift_xpath=SHIFT_G_ON_XPATH,
        shift='晚班',
        on=True,
        msg=GRAVEYARD_MSG
    )
    scheduler.every().day.at(SHIFT_INFO['晚班']['off']).do(
        clock,
        shift_xpath=SHIFT_G_OFF_XPATH,
        shift='晚班',
        on=False,
        msg=GRAVEYARD_MSG
    )
except Exception:
    logger.error(traceback.format_exc())
    err_logger.error(traceback.format_exc())

# 刪除過期log
scheduler.every().day.at("00:00").do(check_logs)

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
