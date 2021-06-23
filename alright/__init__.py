"""
Alright is unofficial Python wrapper for whatsapp web made as an inspiration from PyWhatsApp
allowing you to send messages, images, video and documents programmatically using Python
"""


import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (UnexpectedAlertPresentException,
                                        NoAlertPresentException,
                                        NoSuchElementException)


class WhatsApp(object):
    def __init__(self):
        self.BASE_URL = 'https://web.whatsapp.com/'
        self.suffix_link = 'https://wa.me/'
        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument('--user-data-dir=./User_Data')
        self.browser = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.browser, 600)
        self.login()
        self.mobile = ''

    def login(self):
        self.browser.get(self.BASE_URL)
        self.browser.maximize_window()

    def get_phone_link(self, mobile) -> str:
        """get_phone_link (), create a link based on whatsapp (wa.me) api

        Args:
            mobile ([type]): [description]

        Returns:
            str: [description]
        """
        return f'{self.suffix_link}{mobile}'

    def catch_alert(self, seconds=3):
        """catch_alert()

            catches any sudden alert
        """
        try:
            WebDriverWait(self.browser, seconds).until(EC.alert_is_present())
            alert = self.browser.switch_to_alert.accept()
            return True
        except Exception as e:
            print(e)
            return False

    def find_user(self, mobile) -> None:
        """find_user()
        Makes a user with a given mobile a current target for the wrapper

        Args:
            mobile ([type]): [description]
        """
        try:
            self.mobile = mobile
            link = self.get_phone_link(mobile)
            self.browser.get(link)
            action_button = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="action-button"]')))
            action_button.click()
            time.sleep(2)
            go_to_web = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="fallback_block"]/div/div/a')))
            go_to_web.click()
            time.sleep(1)
        except UnexpectedAlertPresentException as bug:
            print(bug)
            time.sleep(1)
            self.find_user(mobile)

    def find_by_username(self, username):
        """find_user_by_name ()

        locate existing contact by username or number

        Args:
            username ([type]): [description]
        """
        try:
            search_box = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
            search_box.clear()
            search_box.send_keys(username)
            search_box.send_keys(Keys.ENTER)
        except Exception as bug:
            error = f'Exception raised while finding user {username}\n{bug}'
            print(error)

    def send_message(self, message):
        """send_message ()
        Sends a message to a target user

        Args:
            message ([type]): [description]
        """
        try:
            inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
            input_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, inp_xpath)))
            input_box.send_keys(message + Keys.ENTER)
            print(f"Message sent successfuly to {self.mobile}")
        except (NoSuchElementException, Exception) as bug:
            print(bug)
            print(f'Failed to send a message to {self.mobile}')

        finally:
            print("send_message() finished running ")

    def find_attachment(self):
        clipButton = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="main"]/footer//*[@data-icon="clip"]/..')))
        clipButton.click()

    def send_attachment(self):
        # Waiting for the pending clock icon to disappear
        self.wait.until_not(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="main"]//*[@data-icon="msg-time"]')))

        sendButton = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/span/div/div')))
        sendButton.click()

    def send_picture(self, picture):
        """send_picture ()

        Sends a picture to a target user

        Args:
            picture ([type]): [description]
        """
        try:
            filename = os.path.realpath(picture)
            self.find_attachment()
            # To send an Image
            imgButton = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]/footer//*[@data-icon="attach-image"]/../input')))
            imgButton.send_keys(filename)
            self.send_attachment()
            print(f"Picture has been successfully sent to {self.mobile}")
        except (NoSuchElementException, Exception) as bug:
            print(bug)
            print(f'Failed to send a picture to {self.mobile}')

        finally:
            print("send_picture() finished running ")

    def send_video(self, video):
        """send_video ()

        Sends a video to a target user

        Args:
            video ([type]): [description]
        """
        try:
            filename = os.path.realpath(video)
            self.find_attachment()
            # To send a Video
            video_button = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]/footer//*[@data-icon="attach-image"]/../input')))
            video_button.send_keys(filename)
            self.send_attachment()
            print(f'Video has been successfully sent to {self.mobile}')
        except (NoSuchElementException, Exception) as bug:
            print(bug)
            print(f'Failed to send a video to {self.mobile}')
        finally:
            print("send_video() finished running ")

    def send_file(self, filename):
        """send_file()

        Sends a file to target user

        Args:
            filename ([type]): [description]
        """
        try:
            filename = os.path.realpath(filename)
            self.find_attachment()
            document_button = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]/footer//*[@data-icon="attach-document"]/../input')))
            document_button.send_keys(filename)
            self.send_attachment()
        except (NoSuchElementException, Exception) as bug:
            print(bug)
            print(f'Failed to send a PDF to {self.mobile}')
        finally:
            print("send_file() finished running ")
