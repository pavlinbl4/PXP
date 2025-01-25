# pip install webdriver-manager

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from browser.crome_options import setting_chrome_options


def open_page_with_selenium(url: str):
    service = ChromeService(ChromeDriverManager().install())

    # Инициализируем драйвер с указанными опциями
    driver = webdriver.Chrome(service=service, options=setting_chrome_options())
    # Открываем страницу в браузере

    driver.get(url)

    return driver



