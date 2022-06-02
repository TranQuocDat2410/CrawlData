from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
import time
import matplotlib.pyplot as plt
import numpy as np

def check_exists_by_xpath(xpath,driver):
    try:
        driver.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_id(id,driver):
    try:
        driver.find_element(By.ID,id)
    except NoSuchElementException:
        return False
    return True

def getSymbols():
    symbols_list = list()
    driver = webdriver.Chrome()
    driver.get("https://quotes.vcbs.com.vn/a/exchange.html?symbol=HSX")
    time.sleep(1) 
    symbols = driver.find_elements(By.CLASS_NAME,'StockSymbolEven')
    for symbol in symbols:
        symbols_list.append(symbol.text)
    symbols_list = symbols_list[0:101]
    driver.close()
    return symbols_list


def getDailyStock():
    driver = webdriver.Chrome()
    Symbol_lists = getSymbols()
    for symbol in Symbol_lists:
        close_price_list = list()
        date_list = list()
        driver.get("https://s.cafef.vn/Lich-su-giao-dich-"+symbol+"-1.chn")
        xpath_inputdate = '//*[@id="ctl00_ContentPlaceHolder1_ctl03_dpkTradeDate1_txtDatePicker"]'
        input_date = driver.find_element(By.XPATH,xpath_inputdate)
        input_date.clear()
        input_date.send_keys("01/01/2020")
        xpath_button_nextpage = ['//*[@id="ctl00_ContentPlaceHolder1_ctl03_notHO"]/div/div/table/tbody/tr/td[last()]/a', '//*[@id="ctl00_ContentPlaceHolder1_ctl03_divHO"]/div/div/table/tbody/tr/td[last()]/a']
        time.sleep(1)
        close_price_list.extend(get_price(driver)) 
        date_list.extend(get_date(driver)) 
        for xpath in xpath_button_nextpage:
            while True:
                if (check_exists_by_xpath(xpath,driver)):
                    btn = driver.find_element(By.XPATH, xpath)
                    btn.click()
                    time.sleep(1)
                    close_price_list.extend(get_price(driver))
                    get_date(driver)
                    date_list.extend(get_date(driver))
                else:
                    break

        datetime = list()
        for i in date_list:
            mystr = i[2] + "-" + i[1] + "-" + i[0]
            datetime.append(mystr)
        datetime.reverse()
        print("datetime: ",datetime)
        close_price_list.reverse()
        data = {
                'price': close_price_list
                }
        # print(data)
        dataframe = pd.DataFrame(data= data, index= pd.to_datetime(datetime))
        print(dataframe)
        dataframe.to_csv('close_price/' + symbol + ".csv")

def get_price(driver):
    close_price_list = list()
    for i in range(1,21):
        if (i<10):
            if (i%2 == 1):
                id = 'ctl00_ContentPlaceHolder1_ctl03_rptData2_ctl0'+ str(i) +'_itemTR'
            else:
                id = 'ctl00_ContentPlaceHolder1_ctl03_rptData2_ctl0'+ str(i) +'_altitemTR'
        else:
            if (i%2 == 1):
                id = 'ctl00_ContentPlaceHolder1_ctl03_rptData2_ctl'+ str(i) +'_itemTR'
            else:
                id = 'ctl00_ContentPlaceHolder1_ctl03_rptData2_ctl'+ str(i) +'_altitemTR'
        if (check_exists_by_id(id,driver)):
            row = driver.find_element(By.ID,id)
            price = row.find_elements(By.CLASS_NAME,'Item_Price10')
            text_price = price[1].text
            print(text_price)
            close_price_list.append(float(text_price))
        else:
            break
    return close_price_list

def get_date(driver):
    set_date_list = list()
    for i in range(1,21):
        if (i<10):
            if (i%2 == 1):
                id = 'ctl00_ContentPlaceHolder1_ctl03_rptData2_ctl0'+ str(i) +'_itemTR'
            else:
                id = 'ctl00_ContentPlaceHolder1_ctl03_rptData2_ctl0'+ str(i) +'_altitemTR'
        else:
            if (i%2 == 1):
                id = 'ctl00_ContentPlaceHolder1_ctl03_rptData2_ctl'+ str(i) +'_itemTR'
            else:
                id = 'ctl00_ContentPlaceHolder1_ctl03_rptData2_ctl'+ str(i) +'_altitemTR'
        if (check_exists_by_id(id,driver)):
            row = driver.find_element(By.ID,id)
            date = row.find_elements(By.CLASS_NAME,'Item_DateItem')
            text_date = date[0].text
            set_date = text_date.split('/')
            set_date_list.append(set_date)
        else:
            break
    return set_date_list

getDailyStock()



