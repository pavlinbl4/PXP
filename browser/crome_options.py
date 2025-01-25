from selenium.webdriver.chrome.options import Options


def setting_chrome_options():
    chrome_options = Options()

    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")

    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    chrome_options.add_argument("--ignore-certificate-errors")  # игнорирует ошибки сертификата SSL
    chrome_options.add_argument("--disable-cache")  # отключает кэширование в браузере

    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # невидимость автоматизации
    chrome_options.add_argument(
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/"
        "537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
    return chrome_options
