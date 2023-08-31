"""
m_alright is unofficial Python wrapper for whatsapp web made as an inspiration from PyWhatsApp
allowing you to send messages, images, video and documents programmatically using Python
"""

"""
This changes has been made becuase when i use arabic languge some funcs did not work.
'send_message' func does not work especially with long message.
If you want to add emojis to the message the func will not work correctly.
"""

import os
import sys
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    UnexpectedAlertPresentException,
    NoSuchElementException,
)
from webdriver_manager.chrome import ChromeDriverManager

LOGGER = logging.getLogger()


class WhatsApp(object):
    def __init__(self, browser=None, time_out=600):
        # CJM - 20220419: Added time_out=600 to allow the call with less than 600 sec timeout
        # web.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}")

        self.BASE_URL = "https://web.whatsapp.com/"
        self.suffix_link = "https://web.whatsapp.com/send?phone={mobile}&text&type=phone_number&app_absent=1"

        if not browser:
            browser = webdriver.Chrome(
                ChromeDriverManager().install(),
                options=self.chrome_options,
            )

            handles = browser.window_handles
            for _, handle in enumerate(handles):
                if handle != browser.current_window_handle:
                    browser.switch_to.window(handle)
                    browser.close()

        self.browser = browser
        # CJM - 20220419: Added time_out=600 to allow the call with less than 600 sec timeout
        self.wait = WebDriverWait(self.browser, time_out)
        self.cli()
        self.login()
        self.mobile = ""
        self.group = ""

    @property
    def chrome_options(self):
        chrome_options = Options()
        if sys.platform == "win32":
            chrome_options.add_argument("--profile-directory=Default")
            chrome_options.add_argument("--user-data-dir=C:/Temp/ChromeProfile")
        else:
            chrome_options.add_argument("start-maximized")
            chrome_options.add_argument("--user-data-dir=./User_Data")
        return chrome_options

    def cli(self):
        """
        LOGGER settings  [nCKbr]
        """
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s -- [%(levelname)s] >> %(message)s"
            )
        )
        LOGGER.addHandler(handler)
        LOGGER.setLevel(logging.INFO)

    def login(self):
        self.browser.get(self.BASE_URL)
        self.browser.maximize_window()

    def logout(self):
        prefix = "//div[@id='side']/header/div[2]/div/span/div[3]"
        dots_button = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"{prefix}/div[@role='button']",
                )
            )
        )
        dots_button.click()

        logout_item = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"{prefix}/span/div[1]/ul/li[last()]/div[@role='button']",
                )
            )
        )
        logout_item.click()

    def get_phone_link(self, mobile) -> str:
        """get_phone_link (), create a link based on whatsapp (wa.me) api

        Args:
            mobile ([type]): [description]

        Returns:
            str: [description]
        """
        return self.suffix_link.format(mobile=mobile)

    def catch_alert(self, seconds=3):
        """catch_alert()

        catches any sudden alert
        """
        try:
            WebDriverWait(self.browser, seconds).until(EC.alert_is_present())
            alert = self.browser.switch_to_alert.accept()
            return True
        except Exception as e:
            LOGGER.exception(f"An exception occurred: {e}")
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
            time.sleep(3)
        except UnexpectedAlertPresentException as bug:
            LOGGER.exception(f"An exception occurred: {bug}")
            time.sleep(1)
            self.find_user(mobile)

    def find_by_username(self, username):
        """find_user_by_name ()

        locate existing contact by username or number

        Args:
            username ([type]): [description]
        """
        search_box = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="app"]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]',
                )
            )
        )
        search_box.clear()
        search_box.send_keys(username)
        search_box.send_keys(Keys.ENTER)
        try:
            opened_chat = self.browser.find_elements(
                By.XPATH, '//div[@id="main"]/header/div[2]/div[1]/div[1]/span'
            )
            if len(opened_chat):
                title = opened_chat[0].get_attribute("title")
                if title.upper() == username.upper():
                    LOGGER.info(f'Successfully fetched chat "{username}"')
                return True
            else:
                LOGGER.info(f'It was not possible to fetch chat "{username}"')
                return False
        except NoSuchElementException:
            LOGGER.exception(f'It was not possible to fetch chat "{username}"')
            return False

    def username_exists(self, username):
        """username_exists ()

        Returns True or False whether the contact exists or not, and selects the contact if it exists, by checking if the search performed actually opens a conversation with that contact

        Args:
            username ([type]): [description]
        """
        try:
            search_box = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')
                )
            )
            search_box.clear()
            search_box.send_keys(username)
            search_box.send_keys(Keys.ENTER)
            opened_chat = self.browser.find_element(
                By.XPATH,
                "/html/body/div/div[1]/div[1]/div[4]/div[1]/header/div[2]/div[1]/div/span",
            )
            title = opened_chat.get_attribute("title")
            if title.upper() == username.upper():
                return True
            else:
                return False
        except Exception as bug:
            LOGGER.exception(f"Exception raised while finding user {username}\n{bug}")

    def get_first_chat(self, ignore_pinned=True):
        """get_first_chat()  [nCKbr]

        gets the first chat on the list of chats

        Args:
            ignore_pinned (boolean): parameter that flags if the pinned chats should or not be ignored - standard value: True (it will ignore pinned chats!)
        """
        try:
            search_box = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@id="side"]/div[1]/div/div/div/div')
                )
            )
            search_box.click()
            search_box.send_keys(Keys.ARROW_DOWN)
            chat = self.browser.switch_to.active_element
            time.sleep(1)
            if ignore_pinned:
                while True:
                    flag = False
                    for item in chat.find_elements(By.TAG_NAME, "span"):
                        if "pinned" in item.get_attribute("innerHTML"):
                            flag = True
                            break
                    if not flag:
                        break
                    chat.send_keys(Keys.ARROW_DOWN)
                    chat = self.browser.switch_to.active_element

            name = chat.text.split("\n")[0]
            LOGGER.info(f'Successfully selected chat "{name}"')
            chat.send_keys(Keys.ENTER)

        except Exception as bug:
            LOGGER.exception(f"Exception raised while getting first chat: {bug}")

    def search_chat_by_name(self, query: str):
        """search_chat_name()  [nCKbr]

        searches for the first chat containing the query parameter

        Args:
            query (string): query value to be located in the chat name
        """
        try:
            search_box = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@id="side"]/div[1]/div/div/div/div')
                )
            )
            search_box.click()
            search_box.send_keys(Keys.ARROW_DOWN)
            chat = self.browser.switch_to.active_element

            # excepcitonally acceptable here!
            time.sleep(1)
            flag = False
            prev_name = ""
            name = ""
            while True:
                prev_name = name
                name = chat.text.split("\n")[0]
                if query.upper() in name.upper():
                    flag = True
                    break
                chat.send_keys(Keys.ARROW_DOWN)
                chat = self.browser.switch_to.active_element
                if prev_name == name:
                    break
            if flag:
                LOGGER.info(f'Successfully selected chat "{name}"')
                chat.send_keys(Keys.ENTER)
            else:
                LOGGER.info(f'Could not locate chat "{query}"')
                search_box.click()
                search_box.send_keys(Keys.ESCAPE)

        except Exception as bug:
            LOGGER.exception(f"Exception raised while getting first chat: {bug}")

    def get_list_of_messages(self):
        """get_list_of_messages()

        gets the list of messages in the page
        """
        messages = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="pane-side"]/div[2]/div/div/child::div')
            )
        )

        clean_messages = []
        for message in messages:
            _message = message.text.split("\n")
            if len(_message) == 2:
                clean_messages.append(
                    {
                        "sender": _message[0],
                        "time": _message[1],
                        "message": "",
                        "unread": False,
                        "no_of_unread": 0,
                        "group": False,
                    }
                )
            elif len(_message) == 3:
                clean_messages.append(
                    {
                        "sender": _message[0],
                        "time": _message[1],
                        "message": _message[2],
                        "unread": False,
                        "no_of_unread": 0,
                        "group": False,
                    }
                )
            elif len(_message) == 4:
                clean_messages.append(
                    {
                        "sender": _message[0],
                        "time": _message[1],
                        "message": _message[2],
                        "unread": _message[-1].isdigit(),
                        "no_of_unread": int(_message[-1])
                        if _message[-1].isdigit()
                        else 0,
                        "group": False,
                    }
                )
            elif len(_message) == 5:
                clean_messages.append(
                    {
                        "sender": _message[0],
                        "time": _message[1],
                        "message": "",
                        "unread": _message[-1].isdigit(),
                        "no_of_unread": int(_message[-1])
                        if _message[-1].isdigit()
                        else 0,
                        "group": True,
                    }
                )
            elif len(_message) == 6:
                clean_messages.append(
                    {
                        "sender": _message[0],
                        "time": _message[1],
                        "message": _message[4],
                        "unread": _message[-1].isdigit(),
                        "no_of_unread": int(_message[-1])
                        if _message[-1].isdigit()
                        else 0,
                        "group": True,
                    }
                )
            else:
                LOGGER.info(f"Unknown message format: {_message}")
        return clean_messages

    def check_if_given_chat_has_unread_messages(self, query):
        """check_if_given_chat_has_unread_messages() [nCKbr]

        identifies if a given chat has unread messages or not.

        Args:
            query (string): query value to be located in the chat name
        """
        try:
            list_of_messages = self.get_list_of_messages()
            for chat in list_of_messages:
                if query.upper() == chat["sender"].upper():
                    if chat["unread"]:
                        LOGGER.info(
                            f'Yup, {chat["no_of_unread"]} new message(s) on chat <{chat["sender"]}>.'
                        )
                        return True
                    LOGGER.info(f'There are no new messages on chat "{query}".')
                    return False
            LOGGER.info(f'Could not locate chat "{query}"')

        except Exception as bug:
            LOGGER.exception(f"Exception raised while getting first chat: {bug}")

    def send_message1(self, mobile: str, message: str) -> str:
        # CJM - 20220419:
        #   Send WhatsApp Message With Different URL, NOT using https://wa.me/ to prevent WhatsApp Desktop to open
        #   Also include the Number we want to send to
        #   Send Result
        #   0 or Blank or NaN = Not yet sent
        #   1 = Sent successfully
        #   2 = Number to short
        #   3 = Error or Failure to Send Message
        #   4 = Not a WhatsApp Number
        try:
            # Browse to a "Blank" message state
            self.browser.get(f"https://web.whatsapp.com/send?phone={mobile}&text")

            # This is the XPath of the message textbox
            inp_xpath = (
                '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
            )
            # This is the XPath of the "ok button" if the number was not found
            nr_not_found_xpath = (
                '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/div'
            )

            # If the number is NOT a WhatsApp number then there will be an OK Button, not the Message Textbox
            # Test for both situations -> find_elements returns a List
            ctrl_element = self.wait.until(
                lambda ctrl_self: ctrl_self.find_elements(By.XPATH, nr_not_found_xpath)
                or ctrl_self.find_elements(By.XPATH, inp_xpath)
            )
            # Iterate through the list of elements to test each if they are a textBox or a Button
            for i in ctrl_element:
                if i.aria_role == "textbox":
                    # This is a WhatsApp Number -> Send Message

                    for line in message.split("\n"):
                        i.send_keys(line)
                        ActionChains(self.browser).key_down(Keys.SHIFT).key_down(
                            Keys.ENTER
                        ).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()
                    i.send_keys(Keys.ENTER)

                    msg = f"1 "  # Message was sent successfully
                    # Found alert issues when we send messages too fast, so I called the below line to catch any alerts
                    self.catch_alert()

                elif i.aria_role == "button":
                    # Did not find the Message Text box
                    # BUT we possibly found the XPath of the error "Phone number shared via url is invalid."
                    if i.text == "OK":
                        # This is NOT a WhatsApp Number -> Press enter and continue
                        i.send_keys(Keys.ENTER)
                        msg = f"4 "  # Not a WhatsApp Number

        except (NoSuchElementException, Exception) as bug:
            LOGGER.exception(f"An exception occurred: {bug}")
            msg = f"3 "

        finally:
            LOGGER.info(f"{msg}")
            return msg

    def type_text(self, message):
        """send_message ()
        type a message to a target user

        Args:
            message ([type]): [description]
        """
        try:
            inp_xpath = (
                '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
            )
            input_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, inp_xpath))
            )
            input_box.send_keys(message)
                
            
        except (NoSuchElementException, Exception) as bug:
            LOGGER.exception(f"Failed to send a message to {self.mobile} {self.group} - {bug}")
            LOGGER.info("send_message() finished running!")

    def send_direct_message(self, mobile: str, message: str, saved: bool = True):
        if saved:
            self.find_by_username(mobile)
        else:
            self.find_user(mobile)
        self.send_message(message)
    
    #update
    def find_attachment(self):
        clipButton = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]/footer//*[@data-icon="attach-menu-plus"]/..')
            )
        )
        clipButton.click()
    
    #update
    def send_attachment(self):
        # Waiting for the pending clock icon to disappear
        self.wait.until_not(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]//*[@data-icon="msg-time"]')
            )
        )
        time.sleep(0.8)
        # send the message using enter button
        SendButton = self.browser.find_element(
            By.CLASS_NAME, '_3wFFT'
        ).find_element(
            By.CSS_SELECTOR, '[role="button"]'
        )
        # click the button
        SendButton.click()
        
        # Waiting for the pending clock icon to disappear again - workaround for large files or loading videos.
        # Appropriate solution for the presented issue. [nCKbr]
        self.wait.until_not(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]//*[@data-icon="msg-time"]')
            )
        )
    #update
    """
    after writting all text you can put an image to your message,
    the message will send imadately after louding the image without using 'send_enter' func.
    """
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
            
            imgButton = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="main"]/footer//*[@data-testid="mi-attach-media"]//input',
                    )
                )
            )
            imgButton.send_keys(filename)
            self.send_attachment()
            LOGGER.info(f"Picture has been successfully sent to {self.mobile} {self.group}")
        except (NoSuchElementException, Exception) as bug:
            LOGGER.exception(f"Failed to send a message to {self.mobile} - {bug}")
        finally:
            LOGGER.info("send_picture() finished running!")

    def convert_bytes(self, size) -> str:
        # CJM - 2022/06/10:
        # Convert bytes to KB, or MB or GB
        for x in ["bytes", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0

    def convert_bytes_to(self, size, to):
        # CJM - 2022 / 06 / 10:
        # Returns Bytes as 'KB', 'MB', 'GB', 'TB'
        conv_to = to.upper()
        if conv_to in ["BYTES", "KB", "MB", "GB", "TB"]:
            for x in ["BYTES", "KB", "MB", "GB", "TB"]:
                if x == conv_to:
                    return size
                size /= 1024.0

    def send_video(self, video):
        """send_video ()
        Sends a video to a target user
        CJM - 2022/06/10: Only if file is less than 14MB (WhatsApp limit is 15MB)

        Args:
            video ([type]): the video file to be sent.
        """
        try:
            filename = os.path.realpath(video)
            f_size = os.path.getsize(filename)
            x = self.convert_bytes_to(f_size, "MB")
            if x < 14:
                # File is less than 14MB
                self.find_attachment()
                # To send a Video
                video_button = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//*[@id="main"]/footer//*[@data-icon="attach-image"]/../input',
                        )
                    )
                )

                video_button.send_keys(filename)

                self.send_attachment()
                LOGGER.info(f"Video has been successfully sent to {self.mobile}")
            else:
                LOGGER.info(f"Video larger than 14MB")
        except (NoSuchElementException, Exception) as bug:
            LOGGER.exception(f"Failed to send a message to {self.mobile} - {bug}")
        finally:
            LOGGER.info("send_video() finished running!")

    def send_file(self, filename):
        """send_file()

        Sends a file to target user

        Args:
            filename ([type]): [description]
        """
        try:
            filename = os.path.realpath(filename)
            self.find_attachment()
            document_button = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="main"]/footer//*[@data-icon="attach-document"]/../input',
                    )
                )
            )
            document_button.send_keys(filename)
            self.send_attachment()
        except (NoSuchElementException, Exception) as bug:
            LOGGER.exception(f"Failed to send a file to {self.mobile} - {bug}")
        finally:
            LOGGER.info("send_file() finished running!")

    def close_when_message_successfully_sent(self):
        """close_when_message_successfully_sent() [nCKbr]

        Closes the browser window to allow repeated calls when message is successfully sent/received.
        Ideal for recurrent/scheduled messages that would not be sent if a browser is already opened.
        [This may get deprecated when an opened browser verification gets implemented, but it's pretty useful now.]

        Friendly contribution by @euriconicacio.
        """

        LOGGER.info("Waiting for message status update to close browser...")
        try:
            # Waiting for the pending clock icon shows and disappear
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="main"]//*[@data-icon="msg-time"]')
                )
            )
            self.wait.until_not(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="main"]//*[@data-icon="msg-time"]')
                )
            )
        except (NoSuchElementException, Exception) as bug:
            LOGGER.exception(f"Failed to send a message to {self.mobile} - {bug}")
        finally:
            self.browser.close()
            LOGGER.info("Browser closed.")

    def get_last_message_received(self, query: str):
        """get_last_message_received() [nCKbr]

        fetches the last message receive in a given chat, along with couple metadata, retrieved by the "query" parameter provided.

        Args:
            query (string): query value to be located in the chat name
        """
        try:

            if self.find_by_username(query):

                self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//div[@id="main"]/div[3]/div[1]/div[2]/div[3]/child::div[contains(@class,"message-in") or contains(@class,"message-out")][last()]',
                        )
                    )
                )

                time.sleep(
                    3
                )  # clueless on why the previous wait is not respected - we need this sleep to load tha list.

                list_of_messages = self.wait.until(
                    EC.presence_of_all_elements_located(
                        By.XPATH,
                        '//div[@id="main"]/div[3]/div[1]/div[2]/div[3]/child::div[contains(@class,"message-in")]',
                    )
                )

                if len(list_of_messages) == 0:
                    LOGGER.exception(
                        "It was not possible to retrieve the last message - probably it does not exist."
                    )
                else:
                    msg = list_of_messages[-1]

                    is_default_user = self.wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '//div[@id="main"]/header/div[1]/div[1]/div[1]/span',
                            )
                        )
                    ).get_attribute("data-testid")
                    if is_default_user == "default-user":
                        msg_sender = query
                    else:
                        msg_sender = msg.text.split("\n")[0]

                    if len(msg.text.split("\n")) > 1:
                        when = msg.text.split("\n")[-1]
                        msg = (
                            msg.text.split("\n")
                            if "media-play" not in msg.get_attribute("innerHTML")
                            else "Video or Image"
                        )
                    else:
                        when = msg.text.split("\n")[0]
                        msg = "Non-text message (maybe emoji?)"

                    header_group = self.wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '//div[@id="main"]/header/div[1]/div[1]/div[1]/span',
                            )
                        )
                    )
                    header_text = self.wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//div[@id="main"]/header/div[2]/div[2]/span')
                        )
                    )

                    if (
                        header_group.get_attribute("data-testid") == "default-group"
                        and msg_sender.strip() in header_text.text
                    ):

                        LOGGER.info(f"Message sender: {msg_sender}.")
                    elif (
                        msg_sender.strip() != msg[0].strip()
                    ):  # it is not a messages combo
                        LOGGER.info(f"Message sender: {msg_sender}.")
                    else:
                        LOGGER.info(
                            f"Message sender: retrievable from previous messages."
                        )

                    # DISCLAIMER: messages answering other messages carry the previous ones in the text.
                    # Example: Message text: ['John', 'Mary', 'Hi, John!', 'Hi, Mary! How are you?', '14:01']
                    # TODO: Implement 'filter_answer' boolean paramenter to sanitize this text based on previous messages search.

                    LOGGER.info(f"Message text: {msg}.")
                    LOGGER.info(f"Message time: {when}.")

        except Exception as bug:
            LOGGER.exception(f"Exception raised while getting first chat: {bug}")

    def fetch_all_unread_chats(self, limit=True, top=50):
        """fetch_all_unread_chats()  [nCKbr]

        retrieve all unread chats.

        Args:
            limit (boolean): should we limit the counting to a certain number of chats (True) or let it count it all (False)? [default = True]
            top (int): once limiting, what is the *approximate* number of chats that should be considered? [generally, there are natural chunks of 10-22]

        DISCLAIMER: Apparently, fetch_all_unread_chats functionallity works on most updated browser versions
        (for example, Chrome Version 102.0.5005.115 (Official Build) (x86_64)). If it fails with you, please
        consider updating your browser while we work on an alternative for non-updated broswers.

        """
        try:
            counter = 0
            pane = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@id="pane-side"]/div[2]')
                )
            )
            list_of_messages = self.get_list_of_messages()
            read_names = []
            names = []
            names_data = []

            while True:
                last_counter = counter
                for item in list_of_messages:
                    name = item["sender"]
                    if name not in read_names:
                        read_names.append(name)
                        counter += 1
                    if item["unread"]:
                        if name not in names:
                            names.append(name)
                            names_data.append(item)

                pane.send_keys(Keys.PAGE_DOWN)
                pane.send_keys(Keys.PAGE_DOWN)

                list_of_messages = self.get_list_of_messages()
                if (
                    last_counter == counter
                    and counter
                    >= int(
                        self.wait.until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//div[@id="pane-side"]/div[2]')
                            )
                        ).get_attribute("aria-rowcount")
                    )
                    * 0.9
                ):
                    break
                if limit and counter >= top:
                    break

                LOGGER.info(
                    f"The counter value at this chunk is: {counter}."
                )

            if limit:
                LOGGER.info(
                    f"The list of unread chats, considering the first {counter} messages, is: {names}."
                )
            else:
                LOGGER.info(f"The list of all unread chats is: {names}.")
            return names_data

        except Exception as bug:
            LOGGER.exception(f"Exception raised while getting first chat: {bug}")
            return []
        
    #new
    """
    this new fnction to navigate into a group
    by using the left side bar    
    """
    def find_group(self, group: str) -> None:
        self.group = group
        left_bar = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.ID,"pane-side"
                )
            )
        )
        
        spans = left_bar.find_elements(
            By.TAG_NAME,"span"
        )
        for span in spans:
            Text = span.text
            if Text == group:
                span.click()
                break 

    #new 
    """
    this func is to send the message when you finish writting all the message 
    (must be used when you have text just in your messages)
    """
    def send_enter(self):
        inp_xpath = (
            '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
        )
        input_box = self.wait.until(
            EC.presence_of_element_located((By.XPATH, inp_xpath))
        )
        input_box.send_keys(Keys.ENTER)
        LOGGER.info(f"Message sent successfuly to {self.mobile} {self.group}")

    #new
    """
    here you can insert emoji in your text 
    """
    def put_emoji(self, picture):
        # open emoji bar
        button = self.browser.find_element(
            By.CLASS_NAME, "_2lryq"
        ).find_elements(
            By.TAG_NAME, "button"
        )[0]

        ActionChains(self.browser).click(button).perform()
        emoji_list = self.browser.find_element(
            By.CLASS_NAME,  "_157v1"
        ).find_element(
            By.CSS_SELECTOR, '[class="g0rxnol2 thghmljt"]'
        )
        # try 200 times just
        try_times = 1
        while try_times < 200:
            try:
                #try finding the emoji and click to add it
                matching = emoji_list.find_element(
                    By.CSS_SELECTOR, f'[data-testid="{picture}"]'
                )
                ActionChains(self.browser).click(matching).perform()
                
                button = self.browser.find_element(
                    By.CLASS_NAME, "_2lryq"
                ).find_elements(
                    By.TAG_NAME, "button"
                )[0]
                ActionChains(self.browser).click(button).perform()
                break
            except:
                # scrolling to find the emoji if not appear
                scrolling = emoji_list.find_elements(
                    By.TAG_NAME, "div"
                )[0]
                self.browser.execute_script(
                    f"arguments[0].scrollTop += 60", scrolling
                )
                try_times += 1
    #new
    """
    this func move you to a new line
    """
    def new_line(self):
        ActionChains(self.browser).key_down(Keys.SHIFT).key_down(
            Keys.ENTER
        ).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()
        
