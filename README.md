# Stock Alert System

A Python-based stock monitoring system for Raspberry Pi that checks product availability from URLs and sends alerts through Facebook Messenger and GPIO-connected LEDs/buzzer.

## Features

- Monitors multiple URLs for product availability
- Sends alerts via Facebook Messenger
- Visual alerts using RGB LEDs
- Audio alerts using buzzer
- Automatic recovery from errors
- Session persistence for Messenger login

## Hardware Requirements

- Raspberry Pi (any model)
- RGB LED (common cathode)
- Buzzer
- Jumper wires
- Resistors for LEDs

## GPIO Connections 
RGB LED:
Red -> GPIO10
Green -> GPIO9
Blue -> GPIO11
GND -> GND
Buzzer:
Signal -> GPIO17
GND -> GND

## Software Requirements

- Python 3.7 or higher
- Chrome/Chromium browser
- Chrome WebDriver

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd InStock
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Chrome/Chromium browser:
```bash
sudo apt update
sudo apt install chromium-browser chromium-chromedriver
```

## Configuration

1. Configure URLs and markers in `src/config/urls.txt`:
```
# Format: <URL>|<MARKER>|<LED_COLOR>
# LED colors: red=1, green=2, blue=3
https://example.com/product|in stock|1
```

2. Update settings in `src/config/settings.py` if needed:
- GPIO pin assignments
- Alert intervals
- Messenger credentials

## Usage

1. Run the program:
```bash
python -m src.main
```

2. On first run:
- The program will prompt for Facebook login credentials
- Login cookies will be saved for subsequent runs

3. Monitor the logs:
- Check `logs/stock_alert.log` for program status
- Console will show real-time alerts

## LED Color Codes

- Red (1): High priority alerts
- Green (2): Normal availability
- Blue (3): Special offers

## Troubleshooting

1. If Messenger login fails:
   - Delete `config/messenger_cookies.pkl`
   - Restart the program
   - Login again

2. If GPIO errors occur:
   - Check physical connections
   - Verify GPIO pin numbers in settings
   - Ensure proper permissions

3. If program crashes:
   - Check logs for error messages
   - Verify internet connection
   - Ensure Chrome WebDriver is installed

## Error Recovery

The program automatically:
- Retries failed connections
- Recovers from browser crashes
- Reinitializes GPIO on errors
- Maintains alert state across restarts

## Development

Project structure:
```
InStock/
├── src/
│   ├── config/
│   │   ├── settings.py
│   │   └── urls.txt
│   ├── core/
│   │   ├── stock_checker.py
│   │   └── alert_dispatcher.py
│   ├── drivers/
│   │   ├── messenger_driver.py
│   │   └── gpio_driver.py
│   └── utils/
│       ├── html_extractor.py
│       └── logger.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
- Create an issue in the repository