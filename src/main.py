from core.stock_checker import StockChecker
from core.alert_dispatcher import AlertDispatcher
from drivers.messenger_driver import MessengerDriver
from drivers.gpio_driver import GPIODriver
from utils.logger import Logger
import time

class StockAlert:
    def __init__(self):
        self.logger = Logger()
        self.messenger = MessengerDriver()
        self.gpio = GPIODriver()
        
        self.alert_dispatcher = AlertDispatcher(
            messenger_driver=self.messenger,
            gpio_driver=self.gpio
        )
        
        self.stock_checker = StockChecker()

    def initialize(self):
        """Initialize all components and connections"""
        try:
            self.messenger.initialize()
            self.gpio.initialize()
            self.stock_checker.load_urls("config/urls.txt")
            return True
        except Exception as e:
            self.logger.error(f"Initialization failed: {str(e)}")
            return False

    def run(self):
        """Main program loop"""
        while True:
            try:
                if not self.initialize():
                    raise Exception("Failed to initialize components")

                while True:
                    stock_updates = self.stock_checker.check_stock()
                    if stock_updates:
                        self.alert_dispatcher.dispatch_alerts(stock_updates)
                    time.sleep(self.stock_checker.update_interval)

            except Exception as e:
                self.logger.error(f"Error in main loop: {str(e)}")
                self.logger.info("Attempting restart in 30 seconds...")
                time.sleep(30)
                continue

def main():
    alert_system = StockAlert()
    alert_system.run()

if __name__ == "__main__":
    main()
