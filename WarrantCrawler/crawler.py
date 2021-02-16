# coding=UTF-8
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
from enum import IntEnum
import json
import os

class WarrantType(IntEnum):
    NONE = 0
    COW = 1
    BEAR = 2
    BUY = 3
    SELL = 4

def GetStockPrice(soup):
    price = soup.find(id="csvTable2").find("tbody").find(
        "tr").find_all("td", limit=2)[1].text
    return float(price)

def GetDate(s):
    y, m, d = filter(None, re.split("年|月|日", s))
    date = str(int(y)+1911) + '/' + m + '/' + d
    return datetime.strptime(date, "%Y/%m/%d")

def GetType(name):
    t = WarrantType.NONE
    if "牛" in name:
        t = WarrantType.COW
    elif "熊" in name:
        t = WarrantType.BEAR
    elif "購" in name:
        t = WarrantType.BUY
    elif "售" in name:
        t = WarrantType.SELL
    return t

def GetFloat(s):
    replacements = [" ", "\n", ","]
    [s := s.replace(a, "") for a in replacements]
    return float(s)

def GetWarrant(soup):
    trs = soup.find(id="csvTable3").find(
        "tbody").find_all("tr", recursive=False)
    res = []
    today = datetime.today()
    for tr in trs:
        tds = tr.find_all("td", recursive=False)
        date = GetDate(tds[-2].text)
        if (today > date): continue

        temp = lambda: None
        

        temp.date = date
        temp.code = tds[0].a.text
        temp.type = GetType(tds[1].a.text)
        temp.price = GetFloat(tds[3].text)
        temp.strikePrice = GetFloat(tds[5].text)
        temp.purchaseStock = GetFloat(tds[6].text)
        temp.strikeValue = GetFloat(tds[7].text)

        res.append(temp)

    return res

def printWarrant(w):
    print(f"{w.code} {w.date} {w.type} {w.price} {w.strikePrice}")

def Main():
    global driver
    with open(os.path.join(os.getcwd(),'WarrantCrawler', 'setting.json')) as f:
        setting = json.load(f)
    url = f"https://www.twse.com.tw/zh/stockSearch/showStock?stkNo={setting['stock']}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    stockPrice = GetStockPrice(soup)
    res = GetWarrant(soup)
    res = filter(lambda x: x.type == WarrantType.BUY, res)
    res = filter(lambda x: x.strikePrice <= stockPrice, res)
    res = filter(lambda x: x.strikePrice >= 600, res)
    res = filter(lambda x: x.date >= datetime(2021,4,1), res)
    res = sorted(res, key=lambda s: s.date)
    for w in res:
        printWarrant(w)

Main()