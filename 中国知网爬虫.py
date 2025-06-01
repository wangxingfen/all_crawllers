from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import os
def zhiwang():
    options=Options()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0')
    options.add_argument('--headless')
    keyWord=input('请输入论文关键词：示例："机器学习"，然后按回车键确认\n')
    turns=int(input('请输论文页数(每页大概20篇论文)：（示例："1"），然后按回车键确认\n'))
    driver=webdriver.Firefox(options=options)
    url='https://data.oversea.cnki.net/'
    driver.get(url=url)
    #time.sleep(1)
    wait=WebDriverWait(driver,10)
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="txt_SearchText"]'))).send_keys(keyWord)
    #driver.find_element(By.XPATH,'//*[@id="txt_SearchText"]').send_keys(keyWord)
    driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[2]/div[1]/input[2]').click()
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="CF"]'))).click()
    #driver.find_element(By.XPATH,'//*[@id="CF"]').click()
    base_folder = '知网论文合集'
    filename = f'知网论文合集/高引关键词：{keyWord}.csv'
    if  os.path.exists(base_folder)==False:
        os.makedirs(base_folder)
    fieldnames=['题名','作者','来源','发表时间',"数据库",'被引数','下载数',"引用格式",'详情链接']
    with open(filename, 'w', newline='', encoding='utf-8') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writeheader()
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(0.5)
        for i in range(turns):
            article_infos = driver.find_elements(By.XPATH,
                                                '/html/body/div[2]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/div/div/table/tbody/tr')
            for article_info in article_infos:
                try:
                    article_title = article_info.find_element(By.XPATH, './td[2]').text.strip() if article_info.find_element(By.XPATH, './td[2]') else None
                    info_link = article_info.find_element(By.XPATH, './/a').get_attribute('href') if article_info.find_element(By.XPATH, './/a').get_attribute('href') else None
                    article_writer = article_info.find_element(By.XPATH, './td[3]').text.strip() if article_info.find_element(By.XPATH, './td[3]') else None
                    article_source = article_info.find_element(By.XPATH, './td[4]').text.strip() if article_info.find_element(By.XPATH, './td[4]') else None
                    pressed_time = article_info.find_element(By.XPATH, './td[5]').text if article_info.find_element(By.XPATH, './td[5]') else None
                    database = article_info.find_element(By.XPATH, './td[6]').text.strip() if article_info.find_element(By.XPATH, './td[6]') else None
                    quoted_number = article_info.find_element(By.XPATH, './td[7]').text.strip() if article_info.find_element(By.XPATH, './td[7]') else None
                    download_number = article_info.find_element(By.XPATH, './td[8]').text.strip() if article_info.find_element(By.XPATH, './td[8]') else None
                    
                    try:        
                        article_info.find_element(By.XPATH,'./td[9]/a[4]').click()
                        cite_format=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,".layui-layer-content > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)"))).text
                        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,".layui-layer-ico"))).click()
                    except:
                        cite_format=None
                    writer.writerow(
                        {
                            '题名': f'{article_title}',
                            '作者': f'{article_writer}',
                            '来源': f'{article_source}',
                            '发表时间': f'{str(pressed_time)}',
                            "数据库": f'{database}',
                            '被引数': f'{quoted_number}',
                            '下载数': f'{download_number}',
                            '引用格式':f'{cite_format}',
                            '详情链接': f'{info_link}'

                        }
                    )
                except Exception as e:
                    print(e)
                    print('存在一篇论文不符合常规排版')
            try:
                turn_page = driver.find_element(By.XPATH, '//*[@id="PageNext"]')
                turn_page.click()
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                time.sleep(0.5)
            except Exception as e:
                print('没有下一页了')
                break
        current_directory = os.getcwd()
        output_file_path =current_directory + "\\" + filename
        print(f"文件已保存至  {output_file_path}")
if __name__ == "__main__":
    try:
        zhiwang()
    except Exception as e:
        print(e)
        print("请检查你的网络")


