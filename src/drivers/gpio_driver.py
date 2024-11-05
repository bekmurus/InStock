from gpiozero import RGBLED, Buzzer
from ..config.settings import GPIO_CONFIG
from ..config.settings import ALERT_CONFIG
from ..utils.logger import Logger

class GPIODriver:
    def __init__(self):
        self.logger = Logger()
        self.leds = None
        self.buzzer = None
        self.initialized = False

    def initialize(self):
        """Initialize GPIO components"""
        try:
            self.leds = RGBLED(
                red=GPIO_CONFIG['RED_PIN'],
                green=GPIO_CONFIG['GREEN_PIN'],
                blue=GPIO_CONFIG['BLUE_PIN'],
                pwm=GPIO_CONFIG['PWM']
            )
            self.buzzer = Buzzer(GPIO_CONFIG['BUZZER_PIN'])
            self.initialized = True
            self.clear_all()
            return True
        except Exception as e:
            self.logger.error(f"GPIO initialization failed: {str(e)}")
            return False

    def send_alert(self, led_color: int):
        """Trigger LED and buzzer alert"""
        if not self.initialized:
            return False
            
        try:
            self.leds._leds[led_color].on()
            self.buzzer.blink(
                on_time=ALERT_CONFIG['SLEEP_TIME_SEC'],
                off_time=ALERT_CONFIG['SLEEP_TIME_SEC'],
                n=ALERT_CONFIG['BUZZ_LOOPS'],
                background=False
            )
            return True
        except Exception as e:
            self.logger.error(f"Alert triggering failed: {str(e)}")
            return False

    def clear_gpio(self, led_color):
        """Turn off specific LED"""
        if self.initialized:
            self.leds._leds[led_color].off()

    def clear_all(self):
        """Turn off all outputs"""
        if self.initialized:
            self.leds.off()
            self.buzzer.off()

    def test_leds(self):
        """Test all LEDs in sequence"""
        if not self.initialized:
            return False
            
        try:
            self.logger.info("Testing LEDs...")
            for led in self.leds._leds:
                led.blink(on_time=0.5, off_time=0.2, n=1, background=False)
            self.logger.info("LED test complete")
            return True
        except Exception as e:
            self.logger.error(f"LED test failed: {str(e)}")
            return False
