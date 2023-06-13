from selenium import webdriver
from selenium.webdriver.common.by import By

from . import MORNING_MSG, NIGHT_MSG, GRAVEYARD_MSG, NAME_COLUMN_ID, CHECK_BOX_ID, TEST
from .function import send_message, get_time_str
from . import logger, err_logger
from datetime import datetime
from fake_useragent import FakeUserAgent
from retry import retry
from time import sleep
import threading
import requests


class ClockBot:

    def __init__(self, url: str, name: str, shift: str, day_off: list) -> None:
        """

        Args:
            url (str): 表單網址
            name (str): 姓名
            shift (str): 班別
            day_off (list): 休假日 (星期幾)
        """
        self.url = url
        self.name = name
        self.shift = shift
        self.day_off = day_off
        self.selenium = False
        self.sleep_sec = 0

    def set_selenium(self, selenium: bool):
        """設置 是否使用selenium

        Args:
            selenium (bool): True為開啟
        """
        self.selenium = selenium

    def set_sleep_sec(self, second: int):
        """設置休眠時間

        Args:
            second (int): 秒數
        """
        self.sleep_sec = second

    def set_duty(self, duty: bool):
        """設置上班下班\n

        上班時間輸入True\n
        下班時間輸入False\n

        Args:
            duty (bool): 上班時間輸入True
        """
        self.duty = duty

    def set_shift_type(self, shift_type: str):
        """設置 班別

        Args:
            shift_type (str): _description_
        """
        self.shift_type = shift_type

    def is_day_off(self) -> bool:
        """今日是否為假日

        計算方式:\n
        晚班 上班 + 1\n
        中班 下班 - 1\n

        Returns:
            bool: _description_
        """
        ''''''
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

    def is_shift(self) -> bool:
        """輸入班別是否為與指定班別相同

        Returns:
            bool: _description_
        """
        return self.shift == self.shift_type

    def set_selenium_info(self,  shift_type: str, name_xpath: str, shift_xpath: str, submit_xpath: str, driver_path=str):
        """設置 selenium 所需資訊

        Args:
            shift_type (str): 班別
            name_xpath (str): 輸入姓名欄位的xpath
            shift_xpath (str): 班別勾選的xpath
            submit_xpath (str): 送出按鈕的xpath
            driver_path (str): driver路徑
        """
        self.shift_type = shift_type
        self.name_xpath = name_xpath
        self.shift_xpath = shift_xpath
        self.submit_xpath = submit_xpath
        self.driver_path = driver_path

    @retry(delay=1)
    def submit_form_by_selenium(self):
        """使用selenium執行打卡

        須先使用 set_selenium_info() 設置所需資訊
        """
        options = webdriver.ChromeOptions()
        # 在背景執行
        options.add_argument('--headless')
        # 使用無痕模式
        options.add_argument("--incognito")
        # remove the DevTools message
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        try:
            driver = webdriver.Chrome(options=options, executable_path=self.driver_path)
            driver.get(self.url)
            driver.find_element(By.XPATH, self.name_xpath).send_keys(self.name)
            driver.find_element(By.XPATH, self.shift).click()
            logger.debug(f'等待 {get_time_str(self.sleep_sec)}')
            sleep(self.sleep_sec)
            s = '上班' if self.duty else '下班'
            if TEST:
                send_message(f'{datetime.now().__format__("%Y-%m-%d %H:%M:%S")} - 測試訊息: {self.name} {self.shift_type} {s} 執行打卡')
            else:
                send_message(f'{datetime.now().__format__("%Y-%m-%d %H:%M:%S")} - {self.name} {self.shift_type} {s} 執行打卡')
            driver.find_element(By.XPATH, self.submit_xpath).click()
            driver.close()
        except Exception as err:
            logger.info(err, exc_info=True)
            err_logger.info(err, exc_info=True)

    def set_requests_info(self, post_url: str, name_id, on_id, off_id, check_box_value):
        """設置資訊 打api進行填入google表單 所需資訊

        Args:
            post_url (str): api網址
            name_id (_type_): 輸入名稱參數的id
            on_id (_type_): 勾選上班的id
            off_id (_type_): 勾選下班的id
            check_box_value (_type_): _description_
        """
        self.post_url = post_url
        self.name_id = name_id
        self.on_id = on_id
        self.check_box_value = check_box_value
        self.off_id = off_id

    def submit_from(self):
        """使用api執行打卡

        須先使用 set_requests_info() 設置所需資訊
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

            logger.debug(f'等待 {get_time_str(self.sleep_sec)}')
            sleep(self.sleep_sec)
            s = '上班' if self.duty else '下班'
            if TEST:
                send_message(f'{datetime.now().__format__("%Y-%m-%d %H:%M:%S")} - 測試訊息: {self.name} {self.shift_type} {s} 執行打卡')
            else:
                send_message(f'{datetime.now().__format__("%Y-%m-%d %H:%M:%S")} - {self.name} {self.shift_type} {s} 執行打卡')
            r = requests.post(
                self.post_url,
                data=form_data,
                headers=user_agent
            )

            debug_msg = f'form_url={self.url}\npost_url={self.post_url}\nform_data={form_data}\n'
            if r.status_code != 200:
                warring_msg = f'檢查 欄位名稱 ID 是否與表單相同\n{NAME_COLUMN_ID}\n{CHECK_BOX_ID}\n{MORNING_MSG},{NIGHT_MSG},{GRAVEYARD_MSG}'
                send_message(f'{datetime.now().__format__("%Y-%m-%d %H:%M:%S")} - \n{debug_msg}\n{warring_msg}')
                logger.error(f'\n{debug_msg}\n{warring_msg}')
            else:
                logger.debug(debug_msg)
        except Exception as err:
            send_message(f'{datetime.now().__format__("%Y-%m-%d %H:%M:%S")} - {err}')
            logger.error(err, exc_info=True)
            err_logger.error(err, exc_info=True)
        return r

    def run(self) -> bool:
        """執行打卡

        Returns:
            bool: 成功執行回傳True 其餘回傳False
        """
        if not self.is_day_off() and self.is_shift():
            if self.selenium:
                logger.info(f'{self.name} 執行打卡 - submit_form_by_selenium')
                threading.Thread(target=self.submit_form_by_selenium).start()
            else:
                logger.info(f'{self.name} 執行打卡 - submit_from')
                threading.Thread(target=self.submit_from).start()
            return True
        else:
            logger.info(f'{self.name} 條件不符不執行打卡 - 假日:{not self.is_day_off()} 班別:{self.is_shift()}')
            return False
