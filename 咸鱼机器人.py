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
def xianyu_bot(query: str) -> str:
    date =time.strftime('%Y-%m-%d')
    print(date)
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    #options.add_argument('--headless')
    options.add_argument(f'user-agent={UserAgent.random}')
    driver=webdriver.Firefox(options=options)
    url="https://www.goofish.com/im?spm=a21ybx.search.sidebar.1.7a9a28bfDVZsjV"
    driver.get(url=url)
    for cookie in web_cookies["xianyu"]:
        driver.add_cookie(cookie)
    driver.get(url=url)
    wait = WebDriverWait(driver, 2000)
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div/div/aside/div/div[2]/div/div[1]/div/div/div[1]"))
    )
    for i in range(1,10):
        scroll_container = driver.find_element(By.CSS_SELECTOR, '.rc-virtual-list-holder')
        driver.execute_script("arguments[0].scrollTop += 200;", scroll_container)
        time.sleep(1)
        users=driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div/div/aside/div/div[2]/div/div[1]/div/div/div")
        for user in users:

            time.sleep(1)
            user.click()
            time.sleep(1)
            actions = ActionChains(driver)
            # 右键点击用户元素
            actions.context_click(user).perform()
            time.sleep(0.2)
            driver.find_element(By.CSS_SELECTOR,"li.ant-dropdown-menu-item:nth-child(2)").click()
            time.sleep(0.2)
            driver.find_element(By.CSS_SELECTOR,"button.ant-btn:nth-child(2)").click()
            time.sleep(1)
            try:
                driver.find_element(By.CSS_SELECTOR,".ant-input").send_keys("你好")
                #driver.find_element(By.CSS_SELECTOR,".sendbox-bottom--O2c5fyIe > button:nth-child(1)").click()
            except NoSuchElementException:
                print("未找到输入框")

if __name__ == '__main__':
    xianyu_bot("")