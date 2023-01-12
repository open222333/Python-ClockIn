from selenium import webdriver
from selenium.webdriver.common.by import By
from . import ERROR_LOG_FILE_PATH, MORNING_MSG, NIGHT_MSG, GRAVEYARD_MSG
from .clock_logger import logger

from retry import retry
from time import sleep
from datetime import datetime

import logging
import traceback

import requests
from fake_useragent import FakeUserAgent


clock_bot_logger = logging.getLogger('clock_bot')
clock_bot_log_handler = logging.FileHandler(ERROR_LOG_FILE_PATH)
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
clock_bot_log_handler.setFormatter(log_formatter)
clock_bot_logger.addHandler(clock_bot_log_handler)


class ClockBot:

    def __init__(self, url, name, shift, day_off) -> None:
        self.url = url
        self.name = name
        self.shift = shift
        self.day_off = day_off
        self.selenium = False
        self.sleep_sec = None

    def set_selenium(self):
        self.selenium = True

    def set_driver_path(self, driver_path: str):
        """設定driver路徑

        Args:
            driver_path (str): driver路徑
        """
        self.driver_path = driver_path

    def set_duty(self, is_on: bool):
        """_summary_

        Args:
            is_on (bool): 上班時間輸入True
        """
        self.duty = is_on

    def set_shift_type(self, shift_type: str):
        self.shift_type = shift_type

    def set_name_xpath(self, name_xpath: str):
        self.name_xpath = name_xpath

    def set_shift_xpath(self, shift_xpath: str):
        self.shift_xpath = shift_xpath

    def set_submit_xpath(self, submit_xpath: str):
        self.submit_xpath = submit_xpath

    def is_day_off(self):
        '''晚班 上班 + 1, 中班 下班 - 1'''
        weekday = datetime.today().isoweekday()
        if self.shift_type == '中班' and self.duty == False:
            weekday = (weekday - 1) % 7
            weekday = 7 if weekday == 0 else weekday
            return weekday in self.day_off
        elif self.shift_type == '晚班' and self.duty == True:
            weekday = (weekday + 1) % 7
            weekday = 7 if weekday == 0 else weekday
            return weekday in self.day_off
        else:
            return weekday in self.day_off

    def is_shift(self):
        return self.shift == self.shift_type

    @retry(delay=1)
    def submit_form_by_selenium(self):
        options = webdriver.ChromeOptions()
        # 在背景執行
        options.add_argument('--headless')
        # 使用無痕模式
        options.add_argument("--incognito")
        # remove the DevTools message
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Chrome(options=options, executable_path=self.driver_path)
        driver.get(self.url)
        driver.find_element(By.XPATH, self.name_xpath).send_keys(self.name)
        driver.find_element(By.XPATH, self.shift).click()
        driver.find_element(By.XPATH, self.submit_xpath).click()
        driver.close()

    def set_requests_info(self, post_url: str, name_id, on_id, off_id, check_box_value):
        self.post_url = post_url
        self.name_id = name_id
        self.on_id = on_id
        self.check_box_value = check_box_value
        self.off_id = off_id

    def set_sleep_sec(self, minute: int):
        self.sleep_sec = minute * 60

    def submit_from(self):
        """須先執行 set_requests_info()
        """
        try:
            ua = FakeUserAgent()

            user_agent = {
                'Referer': self.url,
                'User-Agent': ua.chrome
            }

            form_data = {
                f'entry.{self.name_id}': self.name
            }

            if self.duty:
                form_data[f'entry.{self.on_id}'] = self.check_box_value
            else:
                form_data[f'entry.{self.off_id}'] = self.check_box_value

            r = requests.post(
                self.post_url,
                data=form_data,
                headers=user_agent
            )
            if r.status_code != 200:
                debug_msg = f'form_url={self.url}\npost_url={self.post_url}\nform_data={form_data}\n'
                warring_msg = f'檢查欄位名稱是否與表單一至 {MORNING_MSG}, {NIGHT_MSG}, {GRAVEYARD_MSG}'
                logger.debug(f'{debug_msg}{warring_msg}')

        except Exception:
            clock_bot_logger.error(traceback.format_exc())
        return r

    def run(self):
        if not self.is_day_off() and self.is_shift():
            if self.sleep_sec:
                sleep(self.sleep_sec)
            if self.selenium:
                clock_bot_logger.info(f'{self.name} {self.shift_type} submit_form_by_selenium')
                self.submit_form_by_selenium()
            else:
                clock_bot_logger.info(f'{self.name} {self.shift_type} submit_from')
                self.submit_from()
            return True
        else:
            clock_bot_logger.info(f'{self.name} {self.shift_type} do noting')
            return False


class Listener:

    def __init__(self, target_dir) -> None:
        self.target_dir = target_dir

    def do(self, func, *args, **kwargs):
        func(*args, **kwargs)

    def run():
        while True:
            datetime.now()
            sleep(1)
