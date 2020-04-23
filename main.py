# -*- coding: utf-8 -*-
import yfinance as yf
import re
import subprocess
import sys


def make_date_values_list(hist):
    date_dirty_list = hist.index.values
    date_list = list()
    for i in date_dirty_list:
        date_list.append(re.findall(r'2020-\d\d-\d\d', str(i)))

    date_list = [x for l in date_list for x in l]
    date_list = [i.replace('2020-', '') for i in date_list]
    date_list = [x[-2:] + '/' + x[:2] for x in date_list]
    print(date_list)
    return date_list


def make_price_values_list(hist):
    close_value = list()
    for i in range(10):
        close_value.append(hist['Close'][i])
    print('Clear: ', close_value)
    return close_value


def list_values_convertor(list):
    max_num = max(list)
    min_num = min(list)
    min_num = round(min_num, 2)
    max_num = round(max_num, 2)
    index_min_max = max_num - min_num
    list2 = [((max_num - elements) * 100) / index_min_max for elements in list]
    list3 = [100 - elements for elements in list2]
    list4 = [round(elements, 1) for elements in list3]
    print('Adapted values for AE: ', list4)
    return list4

def get_min_max_middle_last(list):
    min_max_middle = []
    max_value = max(list)
    min_value = min(list)
    middle_value = max_value - ((max_value - min_value) / 2)
    last_value = list[-1]

    min_value_rounded = round(min_value, 2)
    max_value_rounded = round(max_value, 2)
    middle_value_rounded = round(middle_value, 2)
    last_value_rounded = round(last_value, 2)

    min_max_middle.append(min_value_rounded)
    min_max_middle.append(max_value_rounded)
    min_max_middle.append(middle_value_rounded)
    min_max_middle.append(last_value_rounded)
    print('In function: ', min_max_middle)
    return min_max_middle



def write_to_data_file(list4, day_mon_list, name, min_max_middle):
    with open("D:/GitHub/AE_autographics/data.txt", 'w') as file:
        #Цикл создает массив из значений y, который записывается в файл
        i = 1
        for elements in list4:
            file.write('var y{} = ["{}"];'.format(i, elements) + '\n')
            i = i + 1

        var_max = max(list4)
        file.write('var max = ["{}"];'.format(var_max) + '\n')
        file.write('var day_mon = {}'.format(day_mon_list) + '\n')
        file.write('var val_1 = ["{}", "{}", "{}", "{}"];'.format(min_max_middle[0], min_max_middle[1],min_max_middle[2], min_max_middle[3]) + '\n') #min_num, max_num, midle_num, last_point
        file.write('var ticker = ["{}"];'.format(name) + '\n')


def but_runner():
    program = "D:/GitHub/AE_autographics/Make_grf.bat"
    process = subprocess.Popen(program)
    exit_code = process.wait()

    if exit_code == 0:
        print("Success!")
    else:
        print("Error!")


def main():
    url = 'https://finance.yahoo.com/'
    ticker = 'SBER.ME'
    name = 'Test'
    msft = yf.Ticker(ticker)
    hist = msft.history(period="10d")

    date_lst = make_date_values_list(hist)
    values_lst = make_price_values_list(hist)
    values_lst_converted = list_values_convertor(values_lst)
    min_max_middle_last = get_min_max_middle_last(values_lst)

    write_to_data_file(values_lst_converted, date_lst, name, min_max_middle_last)
    but_runner()


if __name__ == '__main__':
    main()