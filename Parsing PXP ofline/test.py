from bs4 import BeautifulSoup


def main():
    html_file = "/Volumes/big4photo/Downloads/Photoxpress_all time report/PhotoXPress - фотоАРХИВ и фотоНОВОСТИ_files/pc_base_data/source_report.html"
    with open(html_file, "r", encoding='cp1251') as input_file:
        soup = BeautifulSoup(input_file, 'lxml')
        buyer = soup.select(
            'body > table:nth-child(1) > tbody > tr > td:nth-child(2) > strong > small > table > tbody > tr:nth-child(2) > td:nth-child(5) > strong > small')
        print(buyer)


if __name__ == '__main__':
    main()
