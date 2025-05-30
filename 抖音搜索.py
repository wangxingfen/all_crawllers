from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import time
def get_douyin_info(query: str, max_results: int = 20) -> str:
    date =time.strftime('%Y-%m-%d')
    print(date)
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_argument('--headless')
    options.add_argument(f'user-agent={UserAgent.random}')
    driver=webdriver.Firefox(options=options)
    url=f"https://www.douyin.com/search/{query}"
    driver.get(url=url)
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "span.gxIUdClv:nth-child(2)").click()
    for i in range(1,max_results):
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    contents_list=[]
    contents=driver.find_elements(By.XPATH,"/html/body/div[2]/div/div/div/div/div[1]/div[2]/div[2]/ul/li/div/a")
    for content in contents:
        try:
            content_list=content.text.split("\n")
            #print(content_list)
            url=content.get_attribute("href")
            if len(content_list)==5:
                content_dict={}
                content_list.append(url)
                content_dict["时长"]=content_list[0]
                content_dict["点赞数"]=content_list[1]
                content_dict["标题"]=content_list[2]
                content_dict["作者"]=content_list[3]
                content_dict["发布时间"]=content_list[4]
                content_dict["链接"]=content_list[5]
                contents_list.append(content_dict)
            elif len(content_list)==6:
                content_dict={}
                content_list.append(url)
                content_dict["时长"]=content_list[1]
                content_dict["点赞数"]=content_list[2]
                content_dict["标题"]=content_list[3]
                content_dict["作者"]=content_list[4]
                content_dict["发布时间"]=content_list[5]
                content_dict["链接"]=content_list[6]
            contents_list.append(content_dict)
        except Exception as e:
            print(e)
        
    return contents_list
if __name__ == "__main__":
    print(get_douyin_info("抖音",max_results=3))