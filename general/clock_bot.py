from selenium import webdriver
from selenium.webdriver.common.by import By

from retry import retry
from time import sleep
from datetime import datetime


class ClockBot:

    def __init__(self, url, name, shift, day_off) -> None:
        self.url = url
        self.name = name
        self.shift = shift
        self.day_off = day_off

    def set_driver_path(self, driver_path: str):
        """設定driver路徑

        Args:
            driver_path (str): driver路徑
        """
        self.driver_path = driver_path

    def set_on(self, on:bool):
        """_summary_

        Args:
            on (bool): 上班時間輸入True
        """
        self.on = on

    def set_shift_type(self, shift_type: str):
        self.shift_type = shift_type

    def set_name_xpath(self, name_xpath: str):
        self.name_xpath = name_xpath

    def set_shift_xpath(self, shift_xpath: str):
        self.shift_xpath = shift_xpath

    def set_submit_xpath(self, submit_xpath: str):
        self.submit_xpath = submit_xpath

    def is_day_off(self):
        '''晚班 上班 - 1, 中班 下班 + 1'''
        weekday = datetime.today().isoweekday()
        if self.shift_type == '中班' and self.on == False:
            weekday = (weekday + 1) % 7
            weekday = 7 if weekday == 0 else weekday
            return weekday in self.day_off
        elif self.shift_type == '晚班' and self.on == True:
            weekday = (weekday - 1) % 7
            weekday = 7 if weekday == 0 else weekday
            return weekday in self.day_off
        else:
            return weekday in self.day_off

    def is_shift(self):
        return self.shift == self.shift_type

    @retry(delay=1)
    def submit_from(self):
        options = webdriver.ChromeOptions()
        # 在背景執行
        options.add_argument('--headless')
        # 使用無痕模式
        options.add_argument("--incognito")

        driver = webdriver.Chrome(options=options, executable_path=self.driver_path)
        driver.get(self.url)
        driver.find_element(By.XPATH, self.name_xpath).send_keys(self.name)
        driver.find_element(By.XPATH, self.shift).click()
        driver.find_element(By.XPATH, self.submit_xpath).click()
        sleep(10)
        driver.close()

    def run(self):
        if not self.is_day_off() and self.is_shift():
            self.submit_from(self.name, self.shift_xpath)
            return True
        return False
