# GPIO Configuration
GPIO_CONFIG = {
    'RED_PIN': 10,
    'GREEN_PIN': 9,
    'BLUE_PIN': 11,
    'BUZZER_PIN': 17,
    'PWM': False
}

# Alert Configuration
ALERT_CONFIG = {
    'UPDATE_RATE_SEC': 6,
    'BUZZ_LOOPS': 5,
    'SLEEP_TIME_SEC': 0.5
}

# Messenger Configuration
MESSENGER_CONFIG = {
    'BASE_URL': 'https://www.messenger.com',
    'COOKIES_PATH': './config/messenger_cookies.pkl',
    'RECIPIENT_ID': '<messenger_id>'  # Default recipient for alerts
}

# Request Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
} 