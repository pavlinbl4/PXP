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

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from browser.chrome_driver import open_page_with_selenium
from get_credentials import Credentials
from save_to_file import save_date_to_file

from loguru import logger

# Получаем путь к директории скрипта
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
log_file_path = os.path.join(script_dir, "pxp_loging.log")

logger.add(log_file_path, format="{time} {level} {message}", level="INFO")


def notification(message):
    title = "PXP report"
    command = f'''
    osascript -e 'display notification "{message}" with title "{title}"'
    '''
    os.system(command)


def main():
    pxp_user, pxp_pass = Credentials().pxp_login, Credentials().pxp_password
    url = 'https://photoxpress.ru/commerce/commerce_base.asp?action=pc'

    try:
        driver = open_page_with_selenium(url)

        authorization(driver, pxp_pass, pxp_user)

        locate_period(driver)

        period = get_sales_report(driver)

        # print(period)
        logger.info(period)
        print(datetime.now().strftime("%Y-%m-%d"))
        logger.info(datetime.now().strftime("%Y-%m-%d"))
        # notification(f"last report date\n\n{period}")

        save_date_to_file(period)

        driver.close()
        driver.quit()
    except Exception as ex:
        print(ex)
        # driver.close()
        # driver.quit()


def get_sales_report(driver):
    driver.switch_to.parent_frame()
    driver.switch_to.frame("right_frame")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type=image]')))
    driver.find_element(By.CSS_SELECTOR, 'input[type=image]').click()
    period = driver.find_element(By.XPATH, "/html/body/table[1]/tbody/tr/td[2]/strong/small/font[2]").text
    return period


def locate_period(driver):
    driver.find_element(By.CSS_SELECTOR, 'input[type=image]').click()
    driver.switch_to.frame("left_frame")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/table[2]/tbody/tr[3]/td[2]/strong/small/a")))
    driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr[3]/td[2]/strong/small/a").click()


# def save_date_to_file(period):
#     if not os.path.exists('reports_date.txt'):
#         try:
#             open('reports_date.txt', "x").close()
#         finally:
#
#             with open('reports_date.txt', 'r') as log_file:
#                 lines = log_file.readlines()
#                 if len(lines) != 0:
#                     last_date = lines[-1].strip()[13:]
#                 else:
#                     last_date = '*'
#             with open('reports_date.txt', 'a') as log_file:
#                 if last_date != period:
#                     log_file.write(f'{datetime.now().strftime("%Y-%m-%d")} - {period}\n')
#                     send_telegram_message("new report in PXP")


def authorization(driver, pxp_pass, pxp_user):
    driver.switch_to.frame("main_frame")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type=text]')))
    login_input = driver.find_element(By.CSS_SELECTOR, 'input[type=text]')
    password_input = driver.find_element(By.CSS_SELECTOR, 'input[type=password]')
    login_input.send_keys(pxp_user)
    password_input.send_keys(pxp_pass)


if __name__ == '__main__':
    main()
