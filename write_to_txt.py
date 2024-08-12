import os.path


def wtrite_to_txt_file(file_path,new_text):
    if os.path.exists(file_path):
        # with open(file_path, 'r') as log_file:
        #     lines = log_file.readlines() # читаю из имеющегося файла
        with open(file_path, 'a') as log_file:
            log_file.write(f"{new_text}\n")
    else:
        with open(file_path, 'w') as log_file:
            log_file.write(f"{new_text}\n")


file_path = '/Volumes/big4photo/Documents/PXP/reports_date_test.txt'
new_text = input()

wtrite_to_txt_file(file_path,new_text)


