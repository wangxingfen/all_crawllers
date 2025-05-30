from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import time
import random
import csv
import os
from web_cookies  import web_cookies
from selenium.common.exceptions import NoSuchElementException
def check_element_exists(driver,i):
    try:
        driver.find_element(By.CSS_SELECTOR, f'div.list-item:nth-child({i}) > div:nth-child(4)')
        return True
    except NoSuchElementException:
        return False
def bilibili_bot(query: str) -> str:
    date =time.strftime('%Y-%m-%d')
    print(date)
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    #options.add_argument('--headless')
    options.add_argument(f'user-agent={UserAgent.random}')
    driver=webdriver.Firefox(options=options)
    url=f"https://message.bilibili.com/#/whisper/"
    driver.get(url=url)
    for cookie in web_cookies["bilibili_chat"]:
        driver.add_cookie(cookie)
    driver.get(url=url)
    time.sleep(1)
    i=0
    #driver.find_element(By.CSS_SELECTOR, 'div.send-box:nth-child(4) > div:nth-child(2) > div:nth-child(1)').send_keys("你好")
    fans=driver.find_elements(By.XPATH,'/html/body/div[3]/div/div[1]/div[2]/div[2]/div[1]/div/div[1]/div[4]/div[2]/div[1]')
                                       #//*[@id="link-message-container"]/div[1]/div[2]/div[2]/div[1]/div/div[1]/div[4]/div[2]/div[1]/div[4]
    scroll_container = driver.find_element(By.CSS_SELECTOR, '.list-container')
    # 使用JavaScript滚动具体元素
    for i in range(1,100):
        driver.execute_script("arguments[0].scrollTop += 200;", scroll_container)
        time.sleep(0.5)
    i=0
    while True:
        if_true=check_element_exists(driver=driver,i=i)
        if if_true:
            driver.find_element(By.CSS_SELECTOR, f'div.list-item:nth-child({i})').click()
            i+=1
            time.sleep(0.5)    
            message=driver.find_element(By.CSS_SELECTOR, '.message-list-content').text
            message_list=message.split('\n')
            print(message_list[-1])
            driver.find_element(By.CSS_SELECTOR, 'div.send-box:nth-child(4) > div:nth-child(2) > div:nth-child(1)').send_keys("你好")
            driver.find_element(By.CSS_SELECTOR, 'div.send-box:nth-child(4) > div:nth-child(3) > button:nth-child(1)').click()
        else:
            #driver.find_element(By.CSS_SELECTOR, f'div.list-item:nth-child({i})').click()
            i+=1
            time.sleep(0.1)
            
    
bilibili_bot("python")