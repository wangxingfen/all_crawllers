from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import time
import random
import csv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json



def get_douyin_topics(page_list=["热度飙升的话题榜"],hours_list=[24],deepth=3):
    """
    page_list:需要爬取的区块： 话题总榜、热度飙升的话题榜
    hours_list:需要爬取的时长：1、24、72、168
    deepth:翻页深度，默认3页,最多99页
    例：page_list=["话题总榜","热度飙升的话题榜"]
        hours_list=[1,24,72,168]
    说明：每次爬取会生成4*2=8个csv文件
    """
    def one2thrree_parse(writer,big_list,fieldnames):
        topic = big_list[0]
        publish_time = big_list[1].replace('创建时间：','')
        hot_points = big_list[2]
        videos_num = big_list[3]
        play_num = big_list[4]
        if "." not in big_list[5]:
            play_num_per_video = big_list[5].replace('万','0000')
        elif "." in big_list[5]:
            play_num_per_video = big_list[5].replace(".","").replace('万','000')
        else:
            play_num_per_video = big_list[5]
        writer.writerow(
                {
                    f'{fieldnames[0]}':f'{topic}',
                    f'{fieldnames[1]}': f'{publish_time}',
                    f'{fieldnames[2]}': f'{hot_points}',
                    f'{fieldnames[3]}': f'{videos_num}',
                    f'{fieldnames[4]}': f'{play_num}',
                    f'{fieldnames[5]}': f'{play_num_per_video}'
                }
            )
    def parse_date(writer,big_list,fieldnames):
        topic = big_list[1]
        publish_time = big_list[2].replace('创建时间：','')
        hot_points = big_list[3]
        videos_num = big_list[4]
        play_num = big_list[5]
        if "." not in big_list[6]:
            play_num_per_video = big_list[6].replace('万','0000')
        elif "." in big_list[6]:
            play_num_per_video = big_list[6].replace(".","").replace('万','000')
        else:
            play_num_per_video = big_list[6]
        writer.writerow(
                {
                    f'{fieldnames[0]}':f'{topic}',
                    f'{fieldnames[1]}': f'{publish_time}',
                    f'{fieldnames[2]}': f'{hot_points}',
                    f'{fieldnames[3]}': f'{videos_num}',
                    f'{fieldnames[4]}': f'{play_num}',
                    f'{fieldnames[5]}': f'{play_num_per_video}'
                }
            )

    #清洗数据
    date =time.strftime('%Y-%m-%d')
    print(date)
    options=Options()
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_argument(f'user-agent={UserAgent.random}')
    #options.headless=True
    driver=webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 10)
    url='https://douhot.douyin.com/square/hotspot?active_tab=hotspot_video&date_window=1'
    driver.get(url=url)
    fieldnames=['话题名称','创建时间','热度值','视频量','播放量','稿均播放量']
    with open("all_cookies.json", "r", encoding="utf-8") as f:
        web_cookies = json.load(f)
    for cookie in web_cookies["douyin_hot"]:
        driver.add_cookie(cookie)
    time.sleep(3)
    fold_path = f'抖音热点/抖音{date}话题合集'
    if not os.path.exists(fold_path):
        os.makedirs(fold_path)
    hours_duration=[1,24,72,168]
    sub_types={"话题总榜":"2001","热度飙升的话题榜":"2002"}
    for page in page_list:
        for hours in hours_list:        
            url=f"https://douhot.douyin.com/square/hotspot?active_tab=hotspot_topic&date_window={hours}&sub_type={sub_types[page]}"
            driver.get(url=url)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#arco-tabs-0-tab-3")))
            print(sub_types[page])
            filename = f'{fold_path}/{hours}小时内{page}.csv'
            with open(filename, 'w', newline='', encoding='utf-8') as csvFile:
                writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
                writer.writeheader()
                #for i in range(10):
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                wait.until(EC.presence_of_element_located((By.XPATH,"//li[contains(@class,'arco-pagination-item arco-pagination-item-next')]")))
                    #driver.execute_script("window.scrollBy(0, {});".format(random.randint(1000, 2000)))
                contents=driver.find_elements(By.XPATH, "/html/body/div[1]/section/main/div/div/div/div/div/div[2]/div[2]/div[2]/div/div[4]/div/div/div[2]/div[1]/div/div/div[1]/div/div/table/tbody/tr")
                                                        #/html/body/div[1]/section/main/div/div/div/div/div/div[2]/div[2]/div[2]/div/div[4]/div/div/div[2]/div[1]/div/div/div[1]/div/div/table/tbody/tr[9]
                for index,content in enumerate(contents):
                    #print(index,content.text)
                    if index>2:
                        try:
                            big_list = content.text.split('\n')
                            
                            if len(big_list)==8:
                                print(big_list)
                                parse_date(writer=writer, big_list=big_list,fieldnames=fieldnames)
                        except Exception as e:
                            print(e)
                    else:
                        try: 
                            big_list = content.text.split('\n')
                            if len(big_list)==7:
                                print(big_list)
                                one2thrree_parse(writer=writer, big_list=big_list,fieldnames=fieldnames)
                        except Exception as e:
                            print(e)
                for i in range(deepth):
                    try:
                        # 方法2：使用contains方法
                        turn_page = driver.find_element(By.XPATH, "//li[contains(@class,'arco-pagination-item arco-pagination-item-next')]")
                        turn_page.click()
                        #time.sleep(random.randint(2,3))
                        #for i in range(10):
                         #   time.sleep(3)
                        time.sleep(1)
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                            #driver.execute_script("window.scrollBy(0, {});".format(random.randint(1000, 2000)))
                        contents=driver.find_elements(By.XPATH, "/html/body/div[1]/section/main/div/div/div/div/div/div[2]/div[2]/div[2]/div/div[4]/div/div/div[2]/div[1]/div/div/div[1]/div/div/table/tbody/tr")
                        for content in contents:
                            if content.text:
                                big_list = content.text.split('\n')
                                if len(big_list) == 8:
                                    parse_date(writer=writer,big_list=big_list,fieldnames=fieldnames)
                    except Exception as e:
                        False
if  __name__ == '__main__':
    get_douyin_topics(page_list=["热度飙升的话题榜"],hours_list=[24],deepth=3)