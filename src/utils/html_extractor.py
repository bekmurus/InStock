import requests
from ..config.settings import HEADERS
from ..utils.logger import Logger

class HTMLExtractor:
    def __init__(self):
        self.logger = Logger()
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def get_html(self, url, timeout=60):
        """
        Fetch HTML content from URL
        Returns tuple (success, content)
        """
        try:
            response = self.session.get(url, timeout=timeout)
            if response.status_code == 200:
                return True, response.text
            else:
                self.logger.error(f"HTTP {response.status_code} for URL: {url}")
                return False, None
                
        except requests.exceptions.Timeout:
            self.logger.error(f"Timeout while fetching {url}")
            return False, None
        except requests.exceptions.ConnectionError:
            self.logger.error(f"Connection error for {url}")
            return False, None
        except Exception as e:
            self.logger.error(f"Unexpected error fetching {url}: {str(e)}")
            return False, None
