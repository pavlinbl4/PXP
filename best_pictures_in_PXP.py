"""
на основании скачанного отчета хочу получить статистику по снимкам в
фотоэкспресс

- сколько заработано на каждом снимке
- снимки которые принесли максимальный доход за весь период
- снмки которые скачивали наибольшее количество раз
- статистика дохода по годам
- покупатель который заплатил больше всего денег

"""

import pandas as pd

data = pd.read_csv("/Volumes/big4photo/Documents/PXP/pxp_all_time_report.csv")
print(data.columns)


def sheet_name(data):  # дата последней продажи
    last_index = len(data.sell_date)
    return data.sell_date[last_index - 1]


# сколько заработано на каждом снимке за весь период

unique_images = data \
    .groupby('image_id') \
    .nunique() \
    .shape[0]
print(f"количество уникальных снимков в отчете продаж - {unique_images}")  # избыточный блок дл проверки

id_image_income = data \
    .groupby('image_id', as_index=False) \
    .aggregate({'income': sum}) \
    .sort_values('income', ascending=False)  # доход со снимка за весь период




# id_image_sales_count = data.image_id \
#       .value_counts()\
#       .to_frame()                            # сколько раз какой снимок был продан

id_image_sales_count = data[['image_id','sell_date']]\
        .groupby('image_id', as_index=False) \
        .nunique()\
    .rename(columns={'sell_date':'sell_count'})       # сколько раз какой снимок был продан



id_image_income_and_sales_count = id_image_sales_count.merge(id_image_income, on='image_id') \
    .sort_values('income',ascending=False)

id_image_income_and_sales_count.to_excel("/Volumes/big4photo/Documents/PXP/image_income_all_time.xlsx", sheet_name=sheet_name(data))



