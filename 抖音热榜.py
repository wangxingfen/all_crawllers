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
def one2thrree_parse(writer,big_list,fieldnames):
    video_duration = big_list[0]
    video_name = big_list[1]
    maker_name = big_list[2]
    maker_fans = big_list[3].replace('粉丝量：','')
    publish_time = big_list[4].replace('发布时间：','')
    hot_points = big_list[5]
    added_play_rate = big_list[6]
    added_likes = big_list[7]
    likes_rate = big_list[8]
    writer.writerow(
            {
                f'{fieldnames[0]}':f'{video_duration}',
                f'{fieldnames[1]}': f'{video_name}',
                f'{fieldnames[2]}': f'{maker_name}',
                f'{fieldnames[3]}': f'{maker_fans}',
                f'{fieldnames[4]}': f'{hot_points}',
                f'{fieldnames[5]}': f'{publish_time}',
                f'{fieldnames[6]}': f'{added_play_rate}',
                f'{fieldnames[7]}': f'{added_likes}',
                f'{fieldnames[8]}': f'{likes_rate}'
            }
        )
def parse_date(writer,big_list,fieldnames):
    video_duration = big_list[1]
    video_name = big_list[2]
    maker_name = big_list[3]
    maker_fans = big_list[4].replace('粉丝量：','')
    publish_time = big_list[5].replace('发布时间：','')
    hot_points = big_list[6]
    added_play_rate = big_list[7]
    added_likes = big_list[8]
    likes_rate = big_list[9]
    writer.writerow(
            {
                f'{fieldnames[0]}':f'{video_duration}',
                f'{fieldnames[1]}': f'{video_name}',
                f'{fieldnames[2]}': f'{maker_name}',
                f'{fieldnames[3]}': f'{maker_fans}',
                f'{fieldnames[4]}': f'{hot_points}',
                f'{fieldnames[5]}': f'{publish_time}',
                f'{fieldnames[6]}': f'{added_play_rate}',
                f'{fieldnames[7]}': f'{added_likes}',
                f'{fieldnames[8]}': f'{likes_rate}'
            }
        )
def douyin_catcher():
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
    url='https://douhot.douyin.com/square/hotspot?active_tab=hotspot_video&date_window=1'
    driver.get(url=url)
    fieldnames=['视频时长','视频名称','作者名称','作者粉丝量','热度值','发布时间','新增播放量','新增点赞量','点赞率']
    time.sleep(1)
    for cookie in web_cookies["douyin_hot"]:
        driver.add_cookie(cookie)
    fold_path = f'抖音热点/抖音{date}热点合集'
    if not os.path.exists(fold_path):
        os.makedirs(fold_path)
    hours_duration=["1","24","72","168"]
    sub_types={"1001":"视频总榜","1002":"低粉爆款","1003":"高完播率","1004":"高涨粉率","1005":"高点赞率"}
    for hours in hours_duration:
        #pages=driver.find_elements(By.XPATH, "/html/body/div[1]/section/main/div/div/div/div/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div[2]/div[2]/div/div/span")
        for page in sub_types:
            #page.click()
            hours="1"
            page="1002"
            url=f"https://douhot.douyin.com/square/hotspot?active_tab=hotspot_video&date_window={hours}&sub_type={page}"
            driver.get(url=url)
            time.sleep(3)
            print(sub_types[page])
            filename = f'{fold_path}/{hours}小时内{sub_types[page]}.csv'
            with open(filename, 'w', newline='', encoding='utf-8') as csvFile:
                writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
                writer.writeheader()
                #for i in range(10):
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                    #driver.execute_script("window.scrollBy(0, {});".format(random.randint(1000, 2000)))
                contents=driver.find_elements(By.XPATH, "/html/body/div[1]/section/main/div/div/div/div/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div[2]/div[1]/div/div/div[1]/div/div/table/tbody/tr")
                for index,content in enumerate(contents):
                    if index>2:
                        try:
                            big_list = content.text.split('\n')
                            if len(big_list)==11:
                                print(big_list)
                                parse_date(writer=writer, big_list=big_list,fieldnames=fieldnames)
                        except Exception as e:
                            print(e)
                    else:
                        try: 
                            big_list = content.text.split('\n')
                            if len(big_list)==10:
                                one2thrree_parse(writer=writer, big_list=big_list,fieldnames=fieldnames)
                        except Exception as e:
                            print(e)
                for i in range(33):
                    try:
                        # 方法2：使用contains方法
                        turn_page = driver.find_element(By.XPATH, "//li[contains(@class,'arco-pagination-item arco-pagination-item-next')]")
                        turn_page.click()
                        #time.sleep(random.randint(2,3))
                        #for i in range(10):
                         #   time.sleep(3)
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(3)
                            #driver.execute_script("window.scrollBy(0, {});".format(random.randint(1000, 2000)))
                        contents=driver.find_elements(By.XPATH, "/html/body/div[1]/section/main/div/div/div/div/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div[2]/div[1]/div/div/div[1]/div/div/table/tbody/tr")
                        for content in contents:
                            if content.text:
                                big_list = content.text.split('\n')
                                if len(big_list) == 11:
                                    parse_date(writer=writer,big_list=big_list,fieldnames=fieldnames)
                    except Exception as e:
                        False
if  __name__ == '__main__':
    douyin_catcher()