# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 19:35:21 2021

@author: Yu-Cheng Liang
"""
import requests
from bs4 import BeautifulSoup
import json
from enum import Enum
import datetime
from dateutil.relativedelta import relativedelta

# example: stock_crawler(Period.Monthly)

class Period(Enum):
    Daily = 'Daily'
    Weekly = 'Weekly'
    Monthly = 'Monthly'

url = 'https://cn.investing.com/instruments/HistoricalDataAjax'

headers = {
        'authority': 'cn.investing.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'accept': 'text/plain, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://cn.investing.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://cn.investing.com/equities/apple-computer-inc-historical-data',
        'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
    }

today = datetime.datetime.now().strftime("%Y/%m/%d")

def stock_crawler(period = Period.Daily):
    if not isinstance(period, Period):
        print('period must be an instance of Period Enum: Daily, Weekly, Monthly')
        return
    if period != Period.Daily: #daily
        st_date = (datetime.datetime.now() - relativedelta(years=1)).strftime("%Y/%m/%d") 
    else:
        st_date = (datetime.datetime.now() - relativedelta(months=1)).strftime("%Y/%m/%d")
    print('start: '+st_date)
    print('end: '+today)
    data = {
      'curr_id': '6408',
      'smlID': '1159963',
      'header': 'AAPL\u5386\u53F2\u6570\u636E',
      'st_date': st_date,
      'end_date': today,
      'interval_sec': period.value,
      'sort_col': 'date',
      'sort_ord': 'DESC',
      'action': 'historical_data'
    }
    res = requests.post(url, headers=headers, data=data)
    soup = BeautifulSoup(res.content, 'html.parser')
    table = soup.find('table', id="curr_table")
    model = BeautifulSoup(str(table), 'html.parser')
    fields = []
    table_data = []
    
    '''get fields name'''
    for tr in model.find_all('tr'):
        for th in tr.find_all('th'):
            fields.append(th.text)
    
    '''get data'''
    for tr in model.find_all('tr'):
        dataum = {}
        for i, td in enumerate(tr.find_all('td')):
            dataum[fields[i]] = td.text
        if dataum:
            table_data.append(dataum)
    print(json.dumps(table_data, indent=4, ensure_ascii=False))





