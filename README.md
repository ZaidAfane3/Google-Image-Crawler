# Google Image Crawler
A simple Python script to download google images using selenium framework.

# Dependencies
* *pip3 install selenium*
* *pip3 install progressbar2*
* *pip3 install urllib3*
* *pip3 install argparse*

# How to use?
1. Selenium requires a driver to interface with the chosen browser, in this script chrome browser was chosen to work with.

    Download chrome webdriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads), (*make sure to download the version that matches you Google Chrome version*).

1. Run this command: ```python3 google_crawler.py [--limit LIMIT] [--query QUERY] [--directory DIRECTORY] [--webdriver WEBDRIVER_PATH] [-all]```

# Example
* ```python3 google_crawler.py --limit 5 --query car --webdriver ~/Desktop/chromedriver```

    This will download 5 car images and save them in the same directory of the script.

* ```python3 google_crawler.py --limit 5 --query car --webdriver ~/Desktop/chromedriver --directory ~/Desktop/cars_images```

    This will download 5 car images and save them in ~/Desktop/car_images directory.

*  ```python3 google_crawler.py --query car --webdriver ~/Desktop/chromedriver --directory ~/Desktop/cars_images -all```

    This will download all found car images and save them in ~/Desktop/car_images directory.
