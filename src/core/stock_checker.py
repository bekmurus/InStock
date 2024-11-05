from ..utils.html_extractor import HTMLExtractor
from ..utils.logger import Logger
import os
from typing import Dict, Set, List, Tuple

class StockChecker:
    def __init__(self):
        self.logger = Logger()
        self.html_extractor = HTMLExtractor()
        self.url_dict: Dict[int, List] = {}  # {id: [url, marker, led_color]}
        self.stock: Set[int] = set()  # Currently in-stock items
        self.update_interval = 6  # seconds

    def load_urls(self, url_file: str) -> bool:
        """Load URLs and markers from configuration file"""
        try:
            self.logger.info("Loading URLs...")
            file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), url_file)
            
            if not os.path.isfile(file_path):
                self.logger.error(f"URL file not found: {file_path}")
                return False

            with open(file_path) as f:
                cnt: int = 0
                for line in f:
                    if line.startswith('#'):
                        continue
                    parts = line.strip().split('|')
                    if len(parts) == 3:             # url|marker|led_color
                        self.url_dict[cnt] = [
                            parts[0].strip(),
                            parts[1].strip(),
                            int(parts[2].strip())
                        ]
                        cnt += 1

            self.logger.info(f"Loaded {len(self.url_dict)} URLs")
            return True

        except Exception as e:
            self.logger.error(f"Error loading URLs: {str(e)}")
            return False

    def check_stock(self) -> List[Tuple[str, str, int]]:
        """Check stock status for all URLs"""
        updates = []
        
        for key, (url, marker, color) in self.url_dict.items():
            try:
                success, html = self.html_extractor.get_html(url)
                if not success:
                    continue

                in_stock = marker in html
                
                if in_stock and key not in self.stock:
                    self.stock.add(key)
                    updates.append((url, marker, color))
                elif not in_stock and key in self.stock:
                    self.stock.remove(key)
                    updates.append((url, marker, -color))  # -color indicates removal

            except Exception as e:
                self.logger.error(f"Error checking {url}: {str(e)}")
                continue

        return updates
