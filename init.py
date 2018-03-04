# -*- coding: utf-8 -*-

import os, time
import urllib.request

code_list = ['sh600000', 'sh600010', 'sh600016', 'sh600028', 'sh600029', 
             'sh600030', 'sh600036', 'sh600048', 'sh600050', 'sh600104', 
             'sh600109', 'sh600111', 'sh600518', 'sh600519', 'sh600795', 
             'sh600837', 'sh600887', 'sh600893', 'sh600999', 'sh601006', 
             'sh601088', 'sh601166', 'sh601169', 'sh601186', 'sh601288', 
             'sh601318', 'sh601328', 'sh601336', 'sh601377', 'sh601390', 
             'sh601398', 'sh601601', 'sh601628', 'sh601668', 'sh601688', 
             'sh601727', 'sh601766', 'sh601800', 'sh601818', 'sh601857', 
             'sh601919', 'sh601988', 'sh601989', 'sh601998']

h_column = ['日期', '股票代码', '名称', '收盘价', '最高价', 
            '最低价', '开盘价', '前收盘', '涨跌额', '涨跌幅', 
            '成交量', '成交金额']

t_column = ['成交时间', '成交价', '价格变动', '成交量(手)', '成交额(元)', '性质']

sina_count = 0

def get_page(url):
    response = urllib.request.urlopen(url)
    page = response.read()
    return page

    
def get_history(stock_code):
    stock_type = stock_code[0:2]
    stock_id = stock_code[2:]
    
    if stock_type == 'sh':
        stock_id = '0' + stock_id
    if stock_type == "sz":
        stock_id = '1' + stock_id
        
    url = 'http://quotes.money.163.com/service/chddata.html?code=%s&start=20150101&end=20151231&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER'%(stock_id)

    page = get_page(url).decode('gb2312').split('\r\n')
    stock_data = page[1:] # 实际数据
    stock_data = [x.split(',') for x in stock_data]
    stock_data = stock_data[0:len(stock_data)-1]

    return stock_data


def get_transaction(stock_code, date, limit_type):
    global sina_count 
    sina_count += 1
    
    if sina_count >= 40:
        print('Sleeping...')
        time.sleep(600)
        sina_count = 0
        
    url = 'http://market.finance.sina.com.cn/downxls.php?date=%s&symbol=%s'%(date, stock_code)
    name = 'csv/%s__%s__%s.csv'%(stock_code, limit_type, date)
    file = os.open(name, os.O_RDWR|os.O_CREAT)
    data = get_page(url).decode('gb2312').split('\r\n\n')
    data = data[0].split('\n')
    data = data[1:]

    for line in enumerate(data):
        line = line[1]
        line = line.split('\t')
        line = line[:-1]
        line = ','.join(line)
        line = line + '\n'
        
        os.write(file, line.encode('utf8'))
        
    os.close(file)
    
    return name;


def init(code_list):
    for code in code_list:
        data = get_history(code)
        print('%s(%s) 完成'%(data[0][2], code))
        
        up_dates = []
        up_limits = {}
        down_dates = []
        down_limits = {}
        file_list = []
        
        for record in data:
            if record[9] != 'None' and float(record[9]) >= 10:
                up_dates.append(record[0])
                key = code +  ' ' + record[0]
                up_limits[key] = record[7]
                file_name = get_transaction(code, record[0], 'up')
                file_list.append(file_name)
            elif record[9] != 'None' and float(record[9]) <= -10:
                down_dates.append(record[0])
                key = code +  ' ' + record[0]
                down_limits[key] = record[7]
                file_name = get_transaction(code, record[0], 'down')
                file_list.append(file_name)
 
        print('涨停日期：%s'%(('无', up_dates)[len(up_dates) != 0]))
        print('跌停日期：%s\n'%(('无', down_dates)[len(down_dates) != 0]))

# 初始化数据，保存为csv格式
init(code_list)

