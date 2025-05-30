from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webpage_deekseek_nami import webpage_deepseek
from web_cookies import web_cookies
import requests
from bs4  import BeautifulSoup
import random
from pixabay import get_pixabay_images
from AIpost.news.news_images import get_image
from PIL import Image
import win32clipboard
import re
from io import BytesIO
from selenium.webdriver.common.action_chains import ActionChains
def day_hot():
    date =time.strftime('%Y-%m-%d')
    print(date)
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_argument('--headless')
    options.add_argument(f'user-agent={UserAgent.random}')
    driver=webdriver.Firefox(options=options)
    url='https://tophub.today/n/b0vmbqAdB1'
    driver.get(url=url)
    wait=WebDriverWait(driver,2000)
    turn_page=wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,"a.btn"))
    )
    driver.execute_script("window.scrollBy(0, 2000);")
    time.sleep(1)
    news_list=[]
    news=driver.find_elements(By.XPATH,"/html/body/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr/td[2]/a")
    for new in news:
        news_list.append(new.text)
    print(news_list)
    return news_list
def drag_and_drop_image(driver, source_element, target_element):
    """
    模拟拖拽图片的功能
    :param driver: WebDriver实例
    :param source_element: 源图片元素
    :param target_element: 目标位置元素
    """
    action = ActionChains(driver)
    # 点击并按住源元素
    action.click_and_hold(source_element)
    # 移动到目标位置
    action.move_to_element(target_element)
    # 释放鼠标
    action.release()
    # 执行动作
    action.perform()

def send_to_clipboard(image_path):
    image = Image.open(image_path)
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]  # 去除 BMP 文件头
    output.close()
    
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()
def gongzhonghao_writer(topic) -> str:
    date =time.strftime('%Y-%m-%d')
    print(date)
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    #options.add_argument('--headless')
    options.add_argument(f'user-agent={UserAgent.random}')
    driver=webdriver.Firefox(options=options)
    try:
        url='https://mp.weixin.qq.com'
        driver.get(url=url)
        time.sleep(1)
        for cookie in web_cookies["gongzhonghao"]:
            driver.add_cookie(cookie)
        driver.get(url=url)
        wait = WebDriverWait(driver, 20)
        turn_page=wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.new-creation__menu-item:nth-child(2)"))
        )
        turn_page.click()
        time.sleep(2)  # 给新窗口加载一些时间
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
        wait = WebDriverWait(driver, 20)
        title_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#title"))
        )
        news=""
        news=webpage_deepseek(query=f"任务：用中文写一篇有关{topic}的最新的新闻。要求：\n1.必须先在书名号内写好一个20字左右的中文标题。然后才用中文写1000字左右的具体段落，接下来的要求也主要围绕具体段落展开。\n2.为每个段落(除了标题)写一小段对段落的艺术性描述（40个字左右）并放在段落开头（不包括标题）的【】里面。\n3.标题与段落、段落之间都必须通过+++换行，段落总共可分为四到八段。", r1=True, websearch=False)
        if len(news)>10:
            news = re.sub(r'(\d+)([。！？，])', r'\2', news)
            print(news)
            title = news.split("+++")[0].replace("《","").replace("》","")
            title_input.send_keys(title)
            driver.find_element(By.CSS_SELECTOR,"#author").send_keys("AGI造梦工坊")
            contents= news.split("+++")[1:]
            for content in contents:
                print(content)
                pic_path = ""
                keyword="花"
                #提取【和】中间的内容
                if "【"  in content and "】" in content:
                    keyword = content.split("【")[1].split("】")[0]
                    print(keyword)
                    pic_path = get_image(prompt=keyword, i=random.randint(0, 1000000))
                    #pic_path=get_pixabay_images(api_key="47054162-b71e0d9aadb68e45d834827c7",query=keyword,per_page=10)
                    send_to_clipboard(pic_path)
                
                driver.find_element(By.CSS_SELECTOR,".ProseMirror").send_keys(content.replace("【"+keyword+"】",""))
                if len(pic_path) > 4:
                    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(1)
            #设置封面
            wait = WebDriverWait(driver, 30)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#js_cover_area"))).click()
            #driver.find_element(By.CSS_SELECTOR,"#js_cover_area").click()
            wait = WebDriverWait(driver, 30)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#js_cover_null > ul:nth-child(1) > li:nth-child(1) > a:nth-child(1)"))).click()
            #driver.find_element(By.CSS_SELECTOR,"#js_cover_null > ul:nth-child(1) > li:nth-child(1) > a:nth-child(1)").click()
            
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".appmsg_content_img_item"))).click()
            driver.find_element(By.CSS_SELECTOR,".weui-desktop-dialog_img-picker > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(1)").click()
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#vue_app > mp-image-product-dialog:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(2) > button:nth-child(1)"))).click()
            #原创按钮
            wait = WebDriverWait(driver, 30)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#js_original"))).click()
            #driver.find_element(By.XPATH,'//*[@id="js_original"]').click()
            wait = WebDriverWait(driver, 30)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".weui-desktop-icon-checkbox"))).click()
            #driver.find_element(By.CSS_SELECTOR,".weui-desktop-icon-checkbox").click()
            driver.find_element(By.CSS_SELECTOR,".claim__original-dialog > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > button:nth-child(1)").click()
            #赞赏按钮
            wait = WebDriverWait(driver, 30)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#js_reward_setting_area"))).click()
            #driver.find_element(By.CSS_SELECTOR,"#js_reward_setting_area").click()
            wait = WebDriverWait(driver, 30)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".recent-select > div:nth-child(2)"))).click()
            #driver.find_element(By.CSS_SELECTOR,".recent-select > div:nth-child(2)").click()
            driver.find_element(By.CSS_SELECTOR,".operate-btn__group > div:nth-child(1) > button:nth-child(1)").click()
            #添加合集
            driver.execute_script("window.scrollBy(0, 500);")
            wait = WebDriverWait(driver, 30)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".js_article_tags_content"))).click()
            #driver.find_element(By.CSS_SELECTOR,".js_article_tags_content").click()
            driver.find_element(By.CSS_SELECTOR,".select-input > span:nth-child(1) > input:nth-child(1)").send_keys("AGI资讯")
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".select-opt-li"))).click()
            driver.find_element(By.CSS_SELECTOR,".album-setting-dialog > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(1)").click()
            #创作来源
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".js_claim_source_desc > span:nth-child(2)"))).click()
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".js_article_setting_claim_items > div:nth-child(1) > label:nth-child(1)"))).click()
            #保存草稿
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#js_submit"))).click()
            time.sleep(2)
            driver.quit()
        else:
            driver.quit()
    except Exception as e:
        print(e)
if __name__ == "__main__":
    #news_list=day_hot()
    gongzhonghao_writer(topic="ai对人类社会塑造的一些冷思考")
