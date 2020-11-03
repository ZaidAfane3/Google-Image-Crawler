from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import argparse
import logging
import os.path
import progressbar
import sys
import time
import urllib.request

SCROLL_PAUSE_TIME = 1.0
logging.basicConfig(level=logging.INFO)


def getArguments():
    logging.info("Getting application agruments")
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "-q", "--query", default="cat", metavar="", help="Google search query"
    )
    parser.add_argument(
        "-d",
        "--directory",
        default="./",
        metavar="",
        help="Directory where to store the images",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=5,
        metavar="",
        help="Maximum number of images to download",
    )
    parser.add_argument(
        "-w",
        "--webdriver",
        default="./webdriver",
        metavar="",
        help="Path to webdriver executable",
    )
    parser.add_argument(
        "--all", default=False, action="store_true", help="Download all found images"
    )
    args = parser.parse_args()

    return args


def loadWebBrowserPage(webdriverPath, query):
    logging.info(
        "Opening https://www.google.co.in/search?q="
        + query
        + "&source=lnms&tbm=isch on Google Chrome"
    )
    # Check whether the webdriver path is correct or not
    if os.path.isfile(webdriverPath) == False:
        logging.error("Webdriver was not found")
        # Terminate the script if the webdriver path is incorrect
        sys.exit()

    driver = webdriver.Chrome(webdriverPath)
    url = "https://www.google.com/search?q=" + query + "&source=lnms&tbm=isch"
    driver.get(url)

    return driver


def scrollToTheBottomAndLoadMoreImages(driver):
    logging.info("Scrolling down to load more images")
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            elements = driver.find_elements_by_tag_name("input")
            found = False
            for i in range(1, len(elements)):
                if elements[i].get_attribute("value") == "Show more results":
                    try:
                        elements[i].click()
                        found = True
                        break
                    except ElementNotInteractableException:
                        pass
            if not found:
                driver.execute_script(
                    "window.scrollTo(0, -document.body.scrollHeight);"
                )
                break
        last_height = new_height


def downloadImages(driver, args):
    images = driver.find_elements_by_class_name("Q4LuWd")
    if args.all:
        args.limit = len(images)

    logging.info("Downloading " + str(args.limit) + " images")
    bar = progressbar.ProgressBar(max_value=args.limit)
    img = 0
    while img < args.limit and img < len(images):
        # Open the image in a new tab and get its url
        ActionChains(driver).key_down(Keys.COMMAND).click(images[img]).key_up(
            Keys.COMMAND
        ).perform()
        driver.switch_to.window(driver.window_handles[1])
        try:
            url = driver.find_element_by_tag_name("img").get_attribute("src")
        except NoSuchElementException:
            logging.error("Url was not found " + url)
            url = ""
            pass

        # Download the image
        try:
            if url != "":
                opener = urllib.request.build_opener()
                opener.addheaders = [("User-agent", "Mozilla/5.0")]
                urllib.request.install_opener(opener)
                fullname = (
                    args.directory
                    + "_".join(args.query.split(" "))
                    + "_"
                    + str(img)
                    + ".jpg"
                )
                urllib.request.urlretrieve(url, fullname)
        except Exception as e:
            logging.error("Failed to download image " + len(img + 1))

        # Return to the main tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        img = img + 1
        bar.update(img)


if __name__ == "__main__":
    args = getArguments()
    driver = loadWebBrowserPage(args.webdriver, args.query)
    scrollToTheBottomAndLoadMoreImages(driver)
    downloadImages(driver, args)
