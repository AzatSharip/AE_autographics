# -*- coding: utf-8 -*-
import yfinance as yf
import re
import subprocess
import sys
import pytz



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
    # handmade_date = ['04/09', '07/09', '08/09', '09/09', '10/09', '11/09', '14/09', '15/09', '16/09', '17/09']
    # return handmade_date


def make_price_values_list(hist):
    close_value = list()
    for i in range(10):
        close_value.append(hist['Close'][i])
    print('Clear: ', close_value)
    return close_value
    # handmade_value = [2197, 2181, 2110, 2142, 2136, 2128, 2209, 2226, 2177, 2160.4]
    # return handmade_value



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


def red_green_plashka(list):
    last_value = list[-1]
    pre_last_value = list[-2]
    if last_value >= pre_last_value:
        plashka = 100
        print('Плашка будет зеленая')
    else:
        plashka = 0
        print('Плашка будет красная')
    return plashka


def write_to_data_file(list4, day_mon_list, name, min_max_middle, plashka=0):
    with open("D:/Personal/GitHub/AE_autographics/data.txt", 'w') as file:
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
        file.write('var plashka = ["{}"];'.format(plashka) + '\n')


def property_to_bat(name):
    if ' ' in name:
        name = name.replace(' ', '_')
    with open("Make_grf.bat", 'w') as file:
        file.write('chcp 1251\n"C:\Program Files\Adobe\Adobe After Effects CC 2018\Support Files\\aerender.exe" -project D:\Personal\GitHub\AE_autographics\grafik.aep -comp render -OMtemplate graf -output D:\Personal\GitHub\AE_autographics\\STOVE\RYNKI_{}.mov'.format(name))


def but_runner():
    program = "D:/Personal/GitHub/AE_autographics/Make_grf.bat"
    process = subprocess.Popen(program)
    exit_code = process.wait()

    if exit_code == 0:
        print("Success!")
    else:
        print("Error!")



def main(names_list):
    for name in names_list:
        url = 'https://finance.yahoo.com/'
        tickers_dict = {
            'Lenta Ltd.': 'LNTA.ME', 'Tesla inc.': 'TSLA', 'Salesforce.com Inc.': 'CRM', 'Exxon Mobil Corp.': 'XOM', 'ПАО СБЕРБАНК': 'SBER.ME', 'ОАО АК АЛРОСА': 'ALRS.ME',
            'ОАО АФК Система': 'AFKS.ME', 'Facebook Inc.': 'FB', 'Microsoft Corp.': 'MSFT', 'Банк ВТБ': 'VTBR.ME', 'ОАО Группа Компаний ПИК': 'PIKK.ME',
            'ПАО Детский мир': 'DSKY.ME', 'QIWI plc': 'QIWI.ME', 'ОАО Мобильные ТелеСистемы': 'MTSS.ME', 'Lenozoloto PAO Pref': 'LNZLP.ME', 'Яндекс': 'YNDX.ME', 'РОС АГРО ПЛС': 'AGRO.ME',
            'Россети': 'RSTI.ME', 'USD-RUB': 'RUB=X', 'ОАО ГМК Норильский никель': 'GMKN.ME', 'Apple inc.': 'AAPL', 'Alibaba Group Holding Limited': 'BABA', 'ПАО Роснефть': 'ROSN.ME',
            'ПАО Газпром': 'GAZP.ME', 'ОАО АНК Башнефть': 'BANE.ME', 'ОАО АНК Башнефть_П': 'BANEP.ME', 'Сургутнефтегаз_П': 'SNGSP.ME', 'ОАО Нефтекамский автозавод': 'NFAZ.ME', 'Мечел': 'MTLR.ME',
            'Twitter Inc.': 'TWTR', 'American Airlines Group': 'AAL', 'Фьючерсы на нефть WTI': 'CL=F', 'Фьючерс на нефть Brent': 'BZ=F', 'Фьючерс на золото': 'GC=F', 'Индекс Мосбиржи': 'IMOEX.ME',
            'Московская биржа': 'MOEX.ME', 'JPMorgan Chase & Co (JPM)': 'JPM', 'S\\&P 500': '^GSPC', 'The Home Depot Inc.': 'HD', 'ОАО Татнефть': 'TATN.ME', 'Юнайтед Компани РУСАЛ Плс': 'RUAL.ME',
            'Johnson & Johnson': 'JNJ', 'Teladoc Health, Inc.': 'TDOC', 'Nasdaq 100': 'NDX', 'Mail.ru Group Limited': 'MAIL.ME', 'Twilio Inc.': 'TWLO', 'ОАО Северсталь': 'CHMF.ME', 'ОАО Аэрофлот': 'AFLT.ME',
            'ОАО НОВАТЭК': 'NVTK.ME', 'TCS Group Holding PLC': 'TCSG.ME'


        }

        ticker = tickers_dict[name]
        msft = yf.Ticker(ticker)
        hist = msft.history(period="20d")

        if len(hist) == 9:
            print(len(hist))
            hist = msft.history(period="11d")
        elif len(hist) == 8:
            print(len(hist))
            hist = msft.history(period="12d")

        date_lst = make_date_values_list(hist)
        values_lst = make_price_values_list(hist)

        # date_lst = ['09/10', '12/10', '13/10', '14/10', '15/10', '16/10', '19/10', '20/10', '21/10', '22/10']
        # values_lst = [2306.4,2324.0,2215.5,2199.5,2208.8,2155.4,2133.9,2156.0,2200.6,2190.6]

        values_lst_converted = list_values_convertor(values_lst)
        min_max_middle_last = get_min_max_middle_last(values_lst)
        plashka = red_green_plashka(values_lst)
        write_to_data_file(values_lst_converted, date_lst, name, min_max_middle_last, plashka)
        property_to_bat(name)
        but_runner()


if __name__ == '__main__':
    main(['Индекс Мосбиржи'])



