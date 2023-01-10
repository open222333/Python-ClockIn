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

    def set_driver_path(self, driver_path):
        # 設定driver
        self.driver_path = driver_path

    def set_name_xpath(self, name_xpath):
        self.name_xpath = name_xpath

    def set_shift_xpath(self, shift_xpath):
        self.shift_xpath = shift_xpath

    def set_submit_xpath(self, submit_xpath):
        self.submit_xpath = submit_xpath

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
        if datetime.today().isoweekday() not in self.day_off:
            self.submit_from(self.name, self.shift_xpath)
            return True
        return False
