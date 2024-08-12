import os
from datetime import datetime
import sys

from send_message_to_telegram import send_telegram_message


def path_to_txt_file():
    # Получаем путь к директории скрипта
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(script_dir, "reports_date.txt")


def save_date_to_file(period):
    report_date_file = path_to_txt_file()
    if not os.path.exists(report_date_file):
        try:
            open(report_date_file, "x").close()
        finally:

            with open(report_date_file, 'r') as log_file:
                lines = log_file.readlines()
                if len(lines) != 0:
                    last_date = lines[-1].strip()[13:]
                else:
                    last_date = '*'
            with open(report_date_file, 'a') as log_file:
                if last_date != period:
                    log_file.write(f'{datetime.now().strftime("%Y-%m-%d")} - {period}\n')
                    send_telegram_message("new report in PXP")

if __name__ == '__main__':
    # print(path_to_txt_file())
    save_date_to_file(period)