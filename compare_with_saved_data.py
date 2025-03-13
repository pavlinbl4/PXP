
"""Если переданное в функцию число не равно числу в текстовом файле,
то функция возвращает True"""
import sys


def compare_with_saved_data(base_dir, int_images_number):
    with open(
            f'{base_dir}/images_on_site.txt',
            'r+') as text_file:
        if text_file.read().strip() != str(int_images_number):
            text_file.seek(0)
            text_file.write(str(int_images_number))
            text_file.truncate()
            return True
        return False

class CompareWithSavedData:
    def __init__(self, base_dir, text_file_name, any_date):
        self.base_dir = base_dir
        self.any_date = any_date
        self.text_file_name = text_file_name

    def compare(self):
        with open(self.text_file_name, 'r+') as text_file:
            if text_file.read().strip() != str(self.any_date):
                text_file.seek(0)
                text_file.write(str(self.any_date))
                text_file.truncate()
                return True
            return False



