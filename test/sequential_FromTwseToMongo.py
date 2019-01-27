#將股票交易資料放進MongoDB資料庫，就不用需要每次從證交所讀取資料
#Refers from https://github.com/jang0820/Stock/blob/master/FromTwseToMongo.py
######################################################

import numpy as np
import requests
import pandas as pd
import datetime
import json
import matplotlib.pyplot as pp
import time,os,sys
from pymongo import MongoClient
#   http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20180817&stockNo=2330

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"log")
# check log folder if exist or not
if not os.path.isdir(dirnamelog):
    os.mkdir(dirnamelog)

sys.path.append(dirnamelib)
import readConfig as readConfig
from logger import logger
import connectMongoDB

global collection

def get_stock_history(date, stock_no):   #從www.twse.com.tw讀取資料
    quotes = []
    #2019/1/27 remark below 3 lines
    #url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=%s&stockNo=%s' % ( date, stock_no)
    #r = requests.get(url)
    #data = r.json()
        
    url = "http://www.twse.com.tw/exchangeReport/STOCK_DAY"
    query_params = {
            'date': date,
            'response': 'json',
            #'type': 'ALL',
            'stockNo': stock_no,
            '_': str(round(time.time() * 1000) - 500)
    }

    # Get json data
    page = requests.get(url, params=query_params)

    if not page.ok:
        #logging.error("Can not get TSE data at {}".format(date_str))
        msg = "Can not get TSE data at {}"
        logger.info(msg.format(date))
        return
    
    data = page.json()
    #print(data)

    transformdata = transform(data['data'])  #進行資料格式轉換
    #print(transformdata)
    return transformdata

def transform_date(date):   #民國轉西元
        y, m, d = date.split('/')
        return str(int(y)+1911) + '/' + m  + '/' + d
    
def transform_data(data):   #將證交所獲得資料進行資料格式轉換
    data[0] = datetime.datetime.strptime(transform_date(data[0]), '%Y/%m/%d')
    data[1] = int(data[1].replace(',', ''))#把千進位的逗點去除
    data[2] = int(data[2].replace(',', ''))
    data[3] = float(data[3].replace(',', ''))
    data[4] = float(data[4].replace(',', ''))
    data[5] = float(data[5].replace(',', ''))
    data[6] = float(data[6].replace(',', ''))
    data[7] = float(0.0 if data[7].replace(',', '') == 'X0.00' else data[7].replace(',', ''))  # +/-/X表示漲/跌/不比價
    data[8] = int(data[8].replace(',', ''))
    return data

def transform(data):   #讀取每一個元素進行資料格式轉換，再產生新的串列
    return [transform_data(d) for d in data]

def genYM(smonth, syear, emonth, eyear):  #產生從syear年smonth月到eyear年emonth月的所有年與月的tuple
    start = 12 * syear + smonth
    end = 12 * eyear + emonth
    for num in range(int(start), int(end) + 1):
        y, m = divmod(num, 12)
        yield y, m

def fetch_data(year: int, month: int, stockno,delay_sec):  #擷取從year-month開始到目前為止的所有交易日資料
    count_element = 0
    data = []
    list_element = []
    
    today = datetime.datetime.today()
    for year, month in genYM(month, year, today.month, today.year): #產生year-month到今天的年與月份，用於查詢證交所股票資料
        if month < 10:
            date = str(year) + '0' + str(month) + '01'  #1到9月
        else:
            date = str(year) + str(month) + '01'   #10月

        print('Get Date: {}'.format(date))
        data = get_stock_history(date, stockno)
        for item in data:  #取出每一天編號為stockno的股票資料
            #print(item)
            if collection.find({ "date": item[0],   #找尋該交易資料是否不存在
                            "stockno": stockno} ).count() == 0:
                    
                dic_element={'date':item[0], 'stockno':stockno, 'shares':item[1], 
                                    'amount':item[2], 'open':item[3], 'high':item[4], 
                                    'low':item[5], 'close':item[6], 'diff':item[7], 'turnover':item[8]};  #製作MongoDB的插入元素    
                list_element.append(dic_element)#append all dic_element for bluck insert

                count_element += 1   #caluate element numbers
                #print(list_element)
        time.sleep(delay_sec)  #延遲delay_sec秒，證交所會根據IP進行流量統計，流量過大會斷線

    if list_element != []:
        collection.insert_many(list_element)#bulk insert all documents
    
    return count_element   

if __name__ == '__main__':
    t0 = time.time()
    count = 0

    configPath=os.path.join(strdirname,"config.ini")
    localReadConfig = readConfig.ReadConfig(configPath)

    mongo_host = localReadConfig.get_MongoDB('mongo_host')
    mongo_db = localReadConfig.get_MongoDB('mongo_db')
    mongo_collection = localReadConfig.get_MongoDB('mongo_collection')
    mongo_username = localReadConfig.get_MongoDB('mongo_username') 
    mongo_password = localReadConfig.get_MongoDB('mongo_password') 

    str_last_year_month = localReadConfig.get_SeymourExcel("last_year_month")
    str_last_year = str_last_year_month.split(',')[0]
    str_last_month = str_last_year_month.split(',')[1]
    str_stkidx =  localReadConfig.get_SeymourExcel("stkidx")
    str_delay_sec = localReadConfig.get_SeymourExcel("delay_sec")

    collection = connectMongoDB.MongoDBConnection.connect_mongo(mongo_host,mongo_db,
                    mongo_collection,mongo_username,mongo_password)   #連線資料庫
    # only for testing - of course do not do drop() in production
    #collection.drop()

    count = fetch_data(int(str_last_year), int(str_last_month), str_stkidx, int(str_delay_sec))   #取出編號stkidx的股票，從str_last_year_month到今天的股價與成交量資料

    msg = '{} collection(s) downloaded in {:.2f} seconds.'
    logger.info(msg.format(count, time.time() - t0))