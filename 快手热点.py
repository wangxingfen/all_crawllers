from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from web_cookies import web_cookies
import time
import os
import csv
def parse_date(writer,big_list,fieldnames):
    hot_topic = big_list[1]
    hot_points = big_list[2].replace('万','')
    hot_topic_num = big_list[3].replace('个','')

    writer.writerow(
            {
                f'{fieldnames[0]}':f'{hot_topic}',
                f'{fieldnames[1]}': f'{hot_points}',
                f'{fieldnames[2]}': f'{hot_topic_num}',
            })
def kuaishou_catcher():
    date =time.strftime('%Y-%m-%d')
    print(date)
    options=Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    url = 'https://cp.kuaishou.com/creative/hot-spot'
    driver.get(url=url)
    time.sleep(1)
    for cookie in web_cookies["kuaishou"]:
        driver.add_cookie(cookie)
    driver.get(url=url)
    time.sleep(1)
    fold_path = f'快手热点/快手{date}热点合集'
    if not os.path.exists(fold_path):
        os.makedirs(fold_path)
    
    pages=["#tab-BAMBOO_NEWS","#tab-BAMBOO_ENTERTAINMENT",'#BAMBOO_KNOWLEDGE']
    for page in pages:
        title=driver.find_element(By.CSS_SELECTOR, page)
        title.click()
        fieldnames=['热点','热度（万）','热点视频数']
        filename=f"{fold_path}/{title.text}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(20):
                try:
                    time.sleep(1)
                    contents=driver.find_elements(By.XPATH, "//tr[contains(@class,'el-table__row')]")
                    for content in contents:
                        parse_date(writer=writer, big_list=content.text.split('\n'),fieldnames=fieldnames)
                    try:
                        content.find_element(By.XPATH, "//button[contains(@class,'btn-next')]").click()
                    except:
                        break
                except  Exception as e:
                    print(e)


if __name__ == '__main__':
    kuaishou_catcher()