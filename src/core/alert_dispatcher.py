from ..drivers.messenger_driver import MessengerDriver
from ..drivers.gpio_driver import GPIODriver
from ..utils.logger import Logger
from typing import List, Tuple

class AlertDispatcher:
    def __init__(self, messenger_driver: MessengerDriver, gpio_driver: GPIODriver):
        self.logger = Logger()
        self.messenger = messenger_driver
        self.gpio = gpio_driver

    def send_alerts(self, updates: List[Tuple[str, str, int]]):
        """Send alerts for stock updates"""
        for url, marker, led_color in updates:
            if led_color > 0:  # Item in stock
                self.messenger.send_alert(url, marker),
                self.gpio.send_alert(led_color - 1) # -1 because led_color is 1-3
            else:  # Item out of stock
                self.gpio.clear_gpio(abs(led_color) - 1) # -1 because led_color is 1-3

    def dispatch_alerts(self, updates: List[Tuple[str, str, int]]):
        """Wrapper for send_alerts"""
        try:
            self.send_alerts(updates)
        except Exception as e:
            self.logger.error(f"Error dispatching alerts: {str(e)}")
