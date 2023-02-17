import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

INSTAGRAM = "https://www.instagram.com"
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
SIMILAR_ACCOUNT = "mateo.kitchen"


class InstaFollower:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(service=Service("D:\Development\chromedriver.exe"), options=chrome_options)

    def login(self):
        self.driver.get(f"{INSTAGRAM}/accounts/login/")
        time.sleep(3)

        # Close cookies pop-up
        try:
            self.driver.find_element(By.CLASS_NAME, "_a9_1").click()
            time.sleep(2)
        except NoSuchElementException:
            pass

        # Log in
        self.driver.find_element(By.NAME, "username").send_keys(USERNAME)
        self.driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(3)

        # Close 'turn on notifications' pop-up
        try:
            self.driver.find_element(By.CLASS_NAME, "_a9_1").click()
            time.sleep(3)
        except NoSuchElementException:
            pass

    def find_followers(self):
        # Go to user's followers
        self.driver.get(f"{INSTAGRAM}/{SIMILAR_ACCOUNT}/followers/")
        time.sleep(5)

        scrollable_popup = self.driver.find_element(By.CLASS_NAME, "_aano")

        # Scroll
        for _ in range(1):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_popup)
            time.sleep(2)

    def follow(self):
        to_follow = self.driver.find_elements(By.XPATH, "//div[contains(@class, '_aano')]//button[contains(@class, '_acas')]")
        for button in to_follow:
            button.click()
            time.sleep(3)

    def unfollow(self):
        """unfollow users who are on your following list"""
        self.driver.get(f"{INSTAGRAM}/{USERNAME}/following/")
        time.sleep(5)

        scrollable_popup = self.driver.find_element(By.CLASS_NAME, "_aano")

        # Scroll
        for _ in range(3):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_popup)
            time.sleep(2)

        to_unfollow = scrollable_popup.find_elements(By.XPATH, "//button[contains(@class, '_acat')]")
        for button in to_unfollow:
            time.sleep(2)
            button.click()
            time.sleep(2)
            self.driver.find_element(By.CLASS_NAME, "_a9-_").click()


bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()
# bot.unfollow()
