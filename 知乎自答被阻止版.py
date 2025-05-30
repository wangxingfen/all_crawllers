from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.keys import Keys
import random
import csv
from selenium.webdriver.support import expected_conditions as EC
import os
from web_cookies  import web_cookies
from selenium.common.exceptions import NoSuchElementException
def zhihu_bot(query: str) -> str:
    date =time.strftime('%Y-%m-%d')
    print(date)
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    #options.add_argument('--headless')
    options.add_argument(f'user-agent={UserAgent.random}')
    driver=webdriver.Firefox(options=options)
    url="https://www.zhihu.com/question/waiting?type=hot"
    driver.get(url=url)
    for cookie in web_cookies["zhihu"]:
        driver.add_cookie(cookie)
    driver.get(url=url)
    wait = WebDriverWait(driver, 2000)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".SearchBar-askButton")))
    time.sleep(1)
    write_answers=driver.find_elements(By.XPATH, "/html/body/div[1]/div/main/div/div[1]/div[2]/div/div[2]/div[1]/a")
    time.sleep(1)
    for write_answer in write_answers:
        url=write_answer.get_attribute("href")
        driver.get(url=url)
        print(url)
        time.sleep(2)
        #driver.close()
        #driver.switch_to.window(driver.window_handles[-1])

if __name__ == "__main__":
    zhihu_bot("")