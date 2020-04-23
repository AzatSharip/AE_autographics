# -*- coding: utf-8 -*-
import yfinance as yf
import re
import subprocess
import sys

url = 'https://finance.yahoo.com/'
ticker = 'SBER.ME'
name = 'ПАО Сбербанк'
msft = yf.Ticker(ticker)


hist = msft.history(period="10d")

date_dirty_list = hist.index.values
date_list = list()
for i in date_dirty_list:
    #print((re.findall(r'2020-\d\d-\d\d', str(i))))
    date_list.append(re.findall(r'2020-\d\d-\d\d', str(i)))
date_list = [x for l in date_list for x in l]
date_list = [i.replace('2020-', '') for i in date_list]
date_list = [i.replace('-', '/') for i in date_list]
day_mon_list = date_list
print(date_list)


close_value = list()
for i in range(10):
    close_value.append(hist['Close'][i])

list = close_value
max_num = max(list)
min_num = min(list)
min_num = round(min_num, 2)
max_num = round(max_num, 2)


index_min_max = max_num - min_num
list2 = [((max_num - elements) * 100) / index_min_max for elements in list]
list3 = [100 - elements for elements in list2]
list4 = [round(elements, 1) for elements in list3]

last_point = list[-1]
midle_num = max_num - ((max_num - min_num) / 2)
midle_num = round(midle_num, 2)

print(midle_num)
print(list, list2, list3, list4, sep='\n')



with open("D:/Personal/GitHub/AE_autographics/data.txt", 'w') as file:

    #Цикл создает массив из значений y, который записывается в файл
    i = 1
    for elements in list4:
        file.write('var y{} = ["{}"];'.format(i, elements) + '\n')
        i = i + 1

    var_max = max(list4)
    file.write('var max = ["{}"];'.format(var_max) + '\n')

    file.write('var day_mon = {}'.format(day_mon_list) + '\n')

    file.write('var val_1 = ["{}", "{}", "{}", "{}"];'.format(min_num, max_num, midle_num, last_point) + '\n')

    file.write('var ticker = ["{}"];'.format(name) + '\n')


program = "D:/Personal/GitHub/AE_autographics/Make_grf.bat"
process = subprocess.Popen(program)
exit_code = process.wait()

if exit_code == 0:
    print("Success!")
else:
    print("Error!")
