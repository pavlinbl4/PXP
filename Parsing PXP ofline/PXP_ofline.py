"""
скрипт, который анализарует скачанный вручную файл отчета фотоэкспресс
и создает файл с данными по проданным снимкам - старый вариант
с использованием парсинга офлайн страницы, заменен на вариант
с использованием пандас

"""

import csv
from bs4 import BeautifulSoup
import os


def write_csv(usefull_data):
    os.makedirs(f"/Volumes/big4photo/Documents/PXP", exist_ok=True)
    with open("/Volumes/big4photo/Documents/PXP/pxp_all_time_report.csv","a") as output_file:
        writer = csv.writer(output_file)
        writer.writerow([usefull_data["image_id"],usefull_data["sell_date"],usefull_data["buyer"],usefull_data["income"]])



def get_data(offline_html):
    with open(offline_html, encoding="cp1251") as input_file:
        pxp = input_file.read()
        soup = BeautifulSoup(pxp,'lxml')
        trs = soup.find('table').find('tbody').find_all('tr')
        trs = trs[:-5]   # отбрасываю нижнюю таблицу где нет информации о снимках
        count = len(trs)
        for i in range(2,count,2):  # прокручиваю только те тэги td где есть информация так как много пустых
            tds = trs[i].find_all('td')
            sell_date = tds[0].find('small').text.strip()
            image_id = tds[2].find('small').text.strip()[2:]
            buyer = tds[4].find('small').text.strip()
            income = tds[14].find('small').text.strip()
            sell_date = sell_date.replace("\xa0", "_")
            usefull_data = {"sell_date": sell_date,
                            "image_id": image_id,
                            "buyer": buyer,
                            "income":income
                            }
            write_csv(usefull_data)  # временно отключил запись в файл
        last_sold_date = usefull_data['sell_date']
        print(f'Дата последней продажи {last_sold_date}')
        print("work completed")

os.makedirs(f"/Volumes/big4photo/Documents/PXP", exist_ok=True)
with open(f"/Volumes/big4photo/Documents/PXP/pxp_all_time_report.csv","a") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(["image_id","sell_date","buyer","income"])

# исходный файл данных содержит информацию о проданных снимках с самого первого на момент создания отчета
offline_html = "/Volumes/big4photo/Downloads/Photoxpress_all time report/PhotoXPress - фотоАРХИВ и фотоНОВОСТИ_files/pc_base_data/source_report.html"
get_data(offline_html)

