from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service

import time


def driver_firefox(url):
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.get(url)
    return driver


if __name__ == '__main__':
    driver = driver_firefox('https://stepik.org/lesson/1140232/step/1?unit=1151905')
    time.sleep(5)
    driver.quit()
