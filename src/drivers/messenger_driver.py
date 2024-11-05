from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
from ..utils.logger import Logger
from ..config.settings import MESSENGER_CONFIG
import pickle
import os
import time

class MessengerDriver:
    def __init__(self):
        self.logger = Logger()
        self.driver = None
        self.cookies_file = MESSENGER_CONFIG['COOKIES_PATH']
        self.base_url = MESSENGER_CONFIG['BASE_URL']
        self.recipient_id = MESSENGER_CONFIG['RECIPIENT_ID']
        self.is_initialized = False

    def initialize(self) -> bool:
        """Initialize the browser and login session"""
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-infobars')
            options.add_argument("--disable-extensions")
            options.add_argument("--no-sandbox")
            options.add_argument('--disable-dev-shm-usage')
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(10)
            
            if self._load_cookies():
                self._verify_session()
            else:
                self._perform_login()
                self._save_cookies()
            
            self.is_initialized = True
            return True
        except Exception as e:
            self.logger.error(f"Messenger initialization failed: {str(e)}")
            return False

    def _load_cookies(self):
        """Load saved cookies if they exist"""
        try:
            cookies_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                self.cookies_file
            )
            if os.path.exists(cookies_path):
                cookies = pickle.load(open(cookies_path, "rb"))
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                return True
        except Exception as e:
            self.logger.error(f"Cookie loading failed: {str(e)}")
        return False

    def _save_cookies(self):
        """Save current session cookies"""
        try:
            cookies_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                self.cookies_file
            )
            os.makedirs(os.path.dirname(cookies_path), exist_ok=True)
            pickle.dump(self.driver.get_cookies(), open(cookies_path, "wb"))
        except Exception as e:
            self.logger.error(f"Cookie saving failed: {str(e)}")

    def _perform_login(self):
        """Perform fresh login"""
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element_by_id("email").send_keys(input("Enter slave email: "))  # input("Enter email: ")
        self.driver.find_element_by_id("pass").send_keys(getpass("Enter slave pass: "))  # getpass("Enter pass: ")
        self.driver.find_element_by_id("loginbutton").click()
        time.sleep(1)
        try:
            while(self.driver.execute_script("return document.readyState") != 'complete'):
                continue
        except:
            self.logger.error("Error Loading Page")

    def _verify_session(self):
        """Verify if current session is valid"""
        try:
            self.driver.get(self.base_url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[role='navigation']"))
            )
            return True
        except:
            return False

    def send_message(self, recipient_id: str, message: str) -> bool:
        """Send message to specified recipient"""
        try:
            if not self.is_initialized:
                if not self.initialize():
                    return False
                
            self.driver.get(f"{self.base_url}/t/{recipient_id}")
            message_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[role='textbox']"))
            )
            message_box.send_keys(f"{message}\n")
            return True
        except Exception as e:
            self.logger.error(f"Message sending failed: {str(e)}")
            self.is_initialized = False
            return False

    def send_alert(self, url: str, marker: str) -> bool:
        """Send stock alert message"""
        message = f"Stock Alert!\nProduct available at: {url}\nMarker: {marker}"
        return self.send_message(self.recipient_id, message)

    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                #os.system('killall chrome')
                pass
