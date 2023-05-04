# Задание 1

import csv
import re

def write_to_csv(file, data):
    with open(file, 'w') as f_n:
        f_n_writer = csv.writer(f_n)
        for nrow in data:
            f_n_writer.writerow(nrow)


def get_data(lst):
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
    for file in lst:
        datafile = open(file)
        for row in datafile:
            row = row.rstrip()
            if re.match('Изготовитель системы', row):
                os_prod_list.append(re.search(r'(Изготовитель системы).\s*(.*)', row).group(2))
            elif re.match('Название ОС', row):
                os_name_list.append(re.search(r'(Название ОС).\s*(.*)', row).group(2))
            elif re.match('Код продукта', row):
                os_code_list.append(re.search(r'(Код продукта).\s*(.*)', row).group(2))
            elif re.match('Тип системы', row):
                os_type_list.append(re.search(r'(Тип системы).\s*(.*)', row).group(2))

    for k in range(len(lst)):
        main_data.append([
            os_prod_list[k],
            os_name_list[k],
            os_code_list[k],
            os_type_list[k]
         ])
    return main_data


if __name__ == "__main__":
    res = get_data(['info_1.txt', 'info_2.txt', 'info_3.txt'])
    write_to_csv('new_file.csv', res)

    with open('new_file.csv') as f_n:
        print(f_n.read())