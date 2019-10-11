#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 17:22:24 2019

@author: adrian
"""
import requests
from bs4 import BeautifulSoup
import re
import urllib.request


class yahooDataScraper:
    def __init__(self, ticker):
        pageContent=requests.get('https://finance.yahoo.com/quote/' + ticker + '/options')
        self.tree = html.fromstring(pageContent.content)
        
    def maturities(self):
        maturities = self.tree.xpath('//*[@id="Col1-1-OptionContracts-Proxy"]/section/div/div[1]')
        return(maturities)
        
pageContent=requests.get('https://finance.yahoo.com/quote/SPY/options')
r = urllib.request.urlopen('https://finance.yahoo.com/quote/SPY/options')
r
print(r)
l = re.split('<option',r)
len(l)
l[15]
pageContent
r.content
soup = BeautifulSoup(r,'html.parser')
soup.prettify()
soup.find_all('option')

options_tables = soup.find_all("table")
print(options_tables)
soup.prettify()[:100]
soup.find_all('select')
pageContent.json()

   //*[@id="Col1-1-OptionContracts-Proxy"]/section/div/div[1]/select/option[1] 
