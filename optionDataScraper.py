#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 22:34:35 2019

@author: adrian
"""
from selenium import webdriver 
from bs4 import BeautifulSoup
import  requests
import numpy as np
import pandas as pd
from teafiles
import time 

class OptionsDataScraper:
    
    def __init__(self, _ticker, _options_data_columns, _wd):
        self.calls_df = None
        self.puts_df = None
        self.ticker = _ticker
        self.base_url = "https://finance.yahoo.com/quote/{}/options".format(self.ticker)
        self.option_data_col_names = _options_data_columns
        self.working_directory = _wd
        print("OptionsDataScraper for {} initialized.".format(self.ticker))
        
    def get_options_maturities(self):
        print("Getting options maturities for {}...".format(self.ticker))
        self.driver = webdriver.Chrome('/usr/local/bin/chromedriver')
        self.driver.get(self.base_url)
        time.sleep(10)
        self.driver.find_elements_by_css_selector('button')[1].click()
        time.sleep(10)
        options_dates = self.driver.find_elements_by_xpath("//option")
        self.options_dates = [date.get_attribute('value') for date in options_dates]
        print("There are {} maturities for {}".format(len(self.options_dates), self.ticker))
        return(self.options_dates)
        
    def get_option_attributes(call_option__html):
        option_data = call_option__html.find_all("td")
        option_data = [elem.getText() for elem in option_data]
        return(option_data)
    
    def get_options_per_maturity(self, maturity_date, get_difference=True):
        print("Getting {} options data for {}.".format(self.ticker, maturity_date))
        data_url = self.base_url + "?date=" + maturity_date
        data_html = requests.get(data_url).content
        content = BeautifulSoup(data_html, "html.parser")
        options_tables = content.find_all("table")
        if len(options_tables) == 2:
            calls = options_tables[0].find_all("tr")[1:]
            calls = [self.get_option_attributes(call) for call in calls]
            puts = options_tables[1].find_all("tr")[1:]
            puts = [self.get_option_attributes(put) for put in puts]
            calls_df = pd.DataFrame(calls, columns = self.option_data_col_names)
            calls_df = calls_df.set_index('Contract')
            puts_df = pd.DataFrame(puts, columns = self.option_data_col_names)
            puts_df = puts_df.set_index('Contract')
            if get_difference:
                if self.calls_df is not None and self.puts_df is not None:
                    calls_new = pd.concat([self.calls_df, calls_df]).drop_duplicates(keep=False).sort_values(by='LastTrade').groupby().first()
                    puts_new = pd.concat([self.puts_df, puts_df]).drop_duplicates(keep=False).sort_values(by='LastTrade').groupby().first()
                    if !calls_new.empty:
                        self.save_to_file(calls_new, maturity_date)
                    if !puts_new.empty:
                        self.save_to_file(puts_new, maturity_date)
                else:
                    print("To run get_difference you need calls and puts first!")
            else:
                self.calls_df = calls_df
                self.puts_df = puts_df
                self.save_to_file(self.calls_df)
                self.save_to_file(self.puts_df)
        else:
            print("No puts or calls for date {}.".format(maturity_date))
        
    def get_options_all(self):
        for maturity_date in self.options_dates:
            get_options_per_maturity(self, maturity_date)


    def save_to_teafile(self):
        
        
option_data_col_names: ['Contract', 'LastTrade','Strike','Price','Bid','Ask','Change','%Change','Volume','OI','ImplVol']
if __name__ == '__main__':
    scraper = OptionsDataScraper('SPY', option_data_col_names)
    scraper.get_options_maturities()
    scraper.get_options_per_maturity('1571011200', get_difference = False)
    scraper.calls_df
