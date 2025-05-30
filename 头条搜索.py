from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import time
import requests
from bs4  import BeautifulSoup
import random
import csv
import os
def get_toutiao_info(query: str, max_results: int = 20) -> str:
    date =time.strftime('%Y-%m-%d')
    print(date)
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_argument('--headless')
    options.add_argument(f'user-agent={UserAgent.random}')
    driver=webdriver.Firefox(options=options)
    i=1
    url=f"https://so.toutiao.com/search?dvpf=pc&source=input&keyword={query}&pd=information&action_type=search_subtab_switch&page_num={i}&from=news&cur_tab_title=news"
    driver.get(url=url)
    toutiao_list=[]
    for i in range(max_results):
        url=f"https://so.toutiao.com/search?dvpf=pc&source=input&keyword={query}&pd=information&action_type=search_subtab_switch&page_num={i}&from=news&cur_tab_title=news"
        driver.get(url=url)
        time.sleep(1)
        contents=driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div/div/div[1]/div/a")
        for content in contents:
            title=content.text
            href=content.get_attribute("href")
            toutiao_list.append((title,href))
    return toutiao_list
    
if  __name__ == '__main__':
    print(get_toutiao_info("抖音",max_results=3))

