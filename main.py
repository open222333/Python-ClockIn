from general.clock_bot import ClockBot
from general.function import get_time_str, send_message
from general import (
    WOKERS_INFO, SHIFT_INFO, FORM_URL,
    NAME_XPATH, SUBMIT_XPATH,
    SHIFT_N_ON_XPATH, SHIFT_N_OFF_XPATH,
    SHIFT_G_ON_XPATH, SHIFT_G_OFF_XPATH,
    SHIFT_M_ON_XPATH, SHIFT_M_OFF_XPATH,
    DRIVER_PATH, USE_SELENIUM,
    POST_URL, CHECK_BOX_ID, NAME_COLUMN_ID,
    MORNING_MSG, NIGHT_MSG, GRAVEYARD_MSG,
    MAX_MINUTE, MIN_MINUTE, TEST
)
from general import logger, err_logger
from datetime import datetime
from random import randint
from time import sleep
import schedule
import sys


def clock(shift_xpath, shift, on, msg):
    try:
        for name, info in WOKERS_INFO.items():
            s = '上班' if on else '下班'
            logger.info(f'{name} {shift} {s}')
            cb = ClockBot(
                url=FORM_URL,
                name=name,
                shift=info['shift'],
                day_off=info['day_off']
            )
            if USE_SELENIUM:
                cb.set_selenium(True)
                cb.set_selenium_info(
                    shift_type=shift,
                    name_xpath=NAME_XPATH,
                    shift_xpath=shift_xpath,
                    submit_xpath=SUBMIT_XPATH,
                    driver_path=DRIVER_PATH
                )
            else:
                cb.set_requests_info(
                    post_url=POST_URL,
                    name_id=NAME_COLUMN_ID,
                    on_id=CHECK_BOX_ID['on'],
                    off_id=CHECK_BOX_ID['off'],
                    check_box_value=msg
                )
            # 設置隨機時間
            cb.set_sleep_sec(randint(MIN_MINUTE * 60, MAX_MINUTE * 60))
            # 設置班別
            cb.set_shift_type(shift)
            # 設置上下班
            cb.set_duty(on)
            cb.run()
    except Exception as err:
        send_message(f'{datetime.now().__format__("%Y-%m-%d %H:%M:%S")} - {err}')
        logger.error(err, exc_info=True)
        err_logger.error(err, exc_info=True)


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
except Exception as err:
    send_message(f'{datetime.now().__format__("%Y-%m-%d %H:%M:%S")} - {err}')
    logger.error(err, exc_info=True)
    err_logger.error(err, exc_info=True)

if __name__ == '__main__':
    keep_sec = 0
    start_datetime = datetime.now().__format__('%Y-%m-%d %H:%M:%S')
    if TEST:
        print(f'測試 開始執行時間: {start_datetime}')
    else:
        print(f'開始執行時間: {start_datetime}')
    while True:
        try:
            scheduler.run_pending()
            bar = f"\r已執行 {get_time_str(keep_sec)}"
            sys.stdout.write(bar)
            sys.stdout.flush()
        except Exception as err:
            logger.error(err, exc_info=True)
            err_logger.error(err, exc_info=True)
        keep_sec += 1
        sleep(1)
