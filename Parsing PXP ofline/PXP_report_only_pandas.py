"""
работаю с отчетом фотоэкспресс с помощью пандас
"""

import pandas as pd


def clear_dataframe(offline_html):  # функция создает отчищенный датафрэйм
    df = pd.read_html(offline_html, header=1)
    cleared_df = df[0]  # возвращается список с датафрэймами нужно взять один из них
    cleared_df.dropna(axis=0, how='all', inplace=True)  # удалены пустые строки
    cleared_df.drop(cleared_df.tail(3).index,
                    inplace=True)  # удаляю строки которые перекрывают колонки и мешают удалить ненужные
    cleared_df.dropna(axis='columns', how='all', inplace=True)  # удалены колонки без данных
    return cleared_df


def report_data_range(df):  # получаю даты диапазона отчета
    day_first = df.iloc[1][0].split()
    day_last = df.iloc[-1][0].split()
    day_first = "_".join(day_first)
    day_last = "_".join(day_last)
    return day_first, day_last 


def write_to_file(df):
    day_first, day_last = report_data_range(df)
    df.to_excel(f"/Volumes/big4photo/Documents/PXP/image_income_{day_first}_-_{day_last}.xlsx", index=False)


offline_html = "/Volumes/big4photo/Downloads/Photoxpress_all time report/PhotoXPress - фотоАРХИВ и фотоНОВОСТИ_files/pc_base_data/source_report.html"
# offline_html = "/Volumes/big4photo/Downloads/Photoxpress_all time report/2021/PhotoXPress - фотоАРХИВ и фотоНОВОСТИ_files/pc_base_data/source_report.html"

df = clear_dataframe(offline_html)
write_to_file(df)
