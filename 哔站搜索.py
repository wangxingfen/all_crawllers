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
def get_bilibili_info(query: str, max_results: int = 20) -> str:
    date =time.strftime('%Y-%m-%d')
    print(date)
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    #options.add_argument('--headless')
    options.add_argument(f'user-agent={UserAgent.random}')
    driver=webdriver.Firefox(options=options)
    url=f"https://search.bilibili.com/all?keyword={query}&order=pubdate"
    driver.get(url=url)
    for cookie in web_cookies["bilibili"]:
        driver.add_cookie(cookie)
    driver.get(url=url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    results=[]
    contents=driver.find_elements(By.XPATH,"/html/body/div[3]/div/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[2]/div[2]/div/a")
    for content in contents:
        href=content.get_attribute("href")
        if len(href)>100:
            continue
        if len(content.text.strip())>0:
            result=f'{content.text.strip()},{href}'
            results.append(result)
    for page in range(2,max_results+1):
        url=f"https://search.bilibili.com/all?keyword={query}&page={page}&order=pubdate"
        driver.get(url=url)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        contents=driver.find_elements(By.XPATH,"/html/body/div[3]/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div/a")
        for content in contents:
            href=content.get_attribute("href")
            if len(href)>100:
                continue
            if len(content.text.strip())>0:
                result=f'{content.text.strip()},{href}'
                results.append(result)
    return results if results else "No results found."
print(get_bilibili_info("python",max_results=4))