"""
Протестированный скрипт, который открывает страницу с
отчетом на сайте Photoxpress и получает информацию о дате составления
отчета
рефакторинг 20220413 - скрипт заносит в текстовый файл дату появления нового отчета
"""
# pip install webdriver-manager
import os
import sys
from datetime import datetime

from loguru import logger
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from browser.chrome_driver import open_page_with_selenium
from get_credentials import Credentials
from send_message_to_telegram import send_telegram_message

# Константы
LOG_FILE = "pxp_logging.log"
REPORTS_FILE = "reports_date.txt"
PXP_URL = 'https://photoxpress.ru/commerce/commerce_base.asp?action=pc'

# Настройка логирования
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
log_file_path = os.path.join(script_dir, LOG_FILE)
logger.add(log_file_path, format="{time} {level} {message}", level="INFO")


def save_date_to_file(period):
    """
    Сохраняет дату отчета в файл, если отчет новый.
    """
    # Если файл не существует, создается автоматически
    with open(REPORTS_FILE, 'a+', encoding='utf-8') as log_file:
        log_file.seek(0)  # Перемещаемся в начало файла
        lines = log_file.readlines()
        last_date = lines[-1].strip()[13:] if lines else '*'  # Получаем последнюю дату

        if last_date != period:
            log_file.write(f'{datetime.now().strftime("%Y-%m-%d")} - {period}\n')
            logger.info("New report date saved.")
            send_telegram_message(f"report date - {period}")


def wait_for_element(driver, by, value, timeout=15):
    """
    Утилита для ожидания появления элемента на странице.
    """
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
    except Exception as ex:
        logger.error(f"Error waiting for element ({by}, {value}): {ex}")
        raise


def authorization(driver, user, password):
    """
    Авторизация на сайте Photoxpress.
    """
    try:
        driver.switch_to.frame("main_frame")
        wait_for_element(driver, By.CSS_SELECTOR, 'input[type=text]')
        driver.find_element(By.CSS_SELECTOR, 'input[type=text]').send_keys(user)
        driver.find_element(By.CSS_SELECTOR, 'input[type=password]').send_keys(password)
        driver.find_element(By.XPATH, '//input[@type="image"]').click()
        logger.info("Authorization successful.")
    except Exception as ex:
        logger.exception(f"Authorization failed -{ex}")
        raise
    return driver


def locate_period(driver):
    """
    Переход к периоду продаж.
    """
    try:
        wait_for_element(driver, By.XPATH, '//frame[@name="left_frame"]', timeout=25)
        driver.switch_to.frame("left_frame")

        wait_for_element(driver, By.XPATH, "//a[text()='Отчет по продажам']")
        driver.find_element(By.XPATH, "//a[text()='Отчет по продажам']").click()

        wait_for_element(driver, By.XPATH, "/html/body/table[2]/tbody/tr[3]/td[2]/strong/small/a")
        driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr[3]/td[2]/strong/small/a").click()
        logger.info("Located report period successfully.")
    except NoSuchElementException as ex:
        logger.exception(f"Error locating report period - {ex}.")
        raise
    return driver


def get_sales_report(driver):
    """
    Получение периода продаж из отчета.
    """
    try:
        driver.switch_to.parent_frame()
        wait_for_element(driver, By.XPATH, '//frame[@name="right_frame"]', timeout=25)
        driver.switch_to.frame("right_frame")

        wait_for_element(driver, By.XPATH, '//input[@type="image"]')
        driver.find_element(By.XPATH, '//input[@type="image"]').click()

        wait_for_element(driver, By.XPATH, "//font[contains(text(), '202')]")
        period = driver.find_element(By.XPATH, "//font[contains(text(), '202')]").text
        logger.info(f"Sales report period: {period}")
        return period
    except NoSuchElementException as ex:
        logger.exception(f"Error retrieving sales report period - {ex}.")
        raise


def main():
    driver = None
    try:
        credentials = Credentials()
        pxp_user = credentials.pxp_login
        pxp_pass = credentials.pxp_password

        driver = open_page_with_selenium(PXP_URL)
        driver = authorization(driver, pxp_user, pxp_pass)
        driver = locate_period(driver)
        period = get_sales_report(driver)

        save_date_to_file(period)
    except Exception as ex:
        logger.exception(f"An error occurred: {ex}")
    finally:
        if driver:
            driver.quit()


if __name__ == '__main__':
    main()
