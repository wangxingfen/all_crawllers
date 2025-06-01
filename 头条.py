from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from PIL import Image
import win32clipboard
import re
from io import BytesIO
import os
import schedule
import time
import random
from openai import OpenAI
import json
import requests
import time
def webpage_deepseek(query: str,r1:bool,websearch:bool) -> str:
    web_cookies={
        "nami":[{'name': 'sdt', 'value': 'fcb305e4-9a43-463a-ad32-f29e0cb9ad7a', 'path': '/', 'domain': 'www.n.cn', 'secure': False, 'httpOnly': False, 'expiry': 1779806024, 'sameSite': 'None'}, {'name': '__guid', 'value': '235210631.1211101878358809300.1748270024833.2832', 'path': '/', 'domain': '.n.cn', 'secure': False, 'httpOnly': False, 'expiry': 1774190024, 'sameSite': 'None'}, {'name': 'Auth-Token', 'value': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtaWQiOiIyMzUyMTA2MzE0NDg2OTg1MTQxMjk2OTU5MDAwMTc0OCIsInFpZCI6IiIsImRldGFpbCI6IjQwMSIsImV4cCI6MTc0ODg3NDgyNn0.BrhXjqEofHgQIGyq90m1DP9vGXXn-xugmBZ4K60VAd0', 'path': '/', 'domain': '.n.cn', 'secure': True, 'httpOnly': True, 'expiry': 1753454024, 'sameSite': 'None'}, {'name': '__quc_silent__', 'value': '1', 'path': '/', 'domain': 'www.n.cn', 'secure': False, 'httpOnly': False, 'expiry': 1748284431, 'sameSite': 'None'}, {'name': 'Q', 'value': 'u%3D360H3439343733%26n%3D%25P9%25RR%25P0%25O6%25P2%25S6%25O6%25NS%26le%3D%26m%3DZGtkWGWOWGWOWGWOWGWOWGWOAwH5%26qid%3D3439343733%26im%3D1_t011c5aa185298a5ccc%26src%3Dpcw_namiso%26t%3D5', 'path': '/', 'domain': '.n.cn', 'secure': False, 'httpOnly': False, 'expiry': 1779806053, 'sameSite': 'None'}, {'name': 'T', 'value': 's%3Da4e9f328cd2db93691fa661c49318381%26t%3D1748270054%26lm%3D0-1%26lf%3D2%26sk%3D9f7f51695d87bcfad18e798f95d48c29%26mt%3D1748270054%26rc%3D%26v%3D2.0%26a%3D1', 'path': '/', 'domain': '.n.cn', 'secure': False, 'httpOnly': True, 'expiry': 1779806053, 'sameSite': 'None'}, {'name': '__DC_monitor_count', 'value': '2', 'path': '/', 'domain': 'www.n.cn', 'secure': False, 'httpOnly': False, 'expiry': 1748356453, 'sameSite': 'None'}, {'name': 'webp', 'value': '1', 'path': '/', 'domain': '.n.cn', 'secure': True, 'httpOnly': False, 'expiry': 1779806054, 'sameSite': 'None'}, {'name': 'test_cookie_enable', 'value': 'null', 'path': '/', 'domain': 'www.n.cn', 'secure': False, 'httpOnly': False, 'sameSite': 'None'}, {'name': '_ga', 'value': 'GA1.1.668181208.1748270026', 'path': '/', 'domain': '.n.cn', 'secure': False, 'httpOnly': False, 'expiry': 1782830054, 'sameSite': 'None'}, {'name': '_ga_F1YB4HZHRB', 'value': 'GS2.1.s1748270026$o1$g1$t1748270054$j32$l0$h1689704614', 'path': '/', 'domain': '.n.cn', 'secure': False, 'httpOnly': False, 'expiry': 1782830054, 'sameSite': 'None'}, {'name': '_ga_BCGTJC5JR6', 'value': 'GS2.1.s1748270026$o1$g1$t1748270054$j32$l0$h0', 'path': '/', 'domain': '.n.cn', 'secure': False, 'httpOnly': False, 'expiry': 1782830054, 'sameSite': 'None'}, {'name': '__DC_sid', 'value': '235210631.3662244083173830700.1748270022131.8706', 'path': '/', 'domain': 'www.n.cn', 'secure': False, 'httpOnly': False, 'expiry': 1748271874, 'sameSite': 'None'}, {'name': '__DC_gid', 'value': '235210631.432552383.1748270022135.1748270074386.2', 'path': '/', 'domain': 'www.n.cn', 'secure': False, 'httpOnly': False, 'expiry': 1782830074, 'sameSite': 'None'}],

    }
    date =time.strftime('%Y-%m-%d')
    print(date)
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_argument('--headless')
    options.add_argument(f'user-agent={UserAgent.random}')
    driver=webdriver.Firefox(options=options)
    url=f"https://www.n.cn/"
    driver.get(url=url)
    time.sleep(1)
    for cookie in web_cookies["nami"]:
        driver.add_cookie(cookie)
    driver.get(url=url)
    wait = WebDriverWait(driver, 2000)
    turn_page=wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "section.w-28px"))
    )
    if r1:
        turn_page.click()
    driver.find_element(By.CSS_SELECTOR,"#composition-input").send_keys(query)
    driver.find_element(By.CSS_SELECTOR,".p-6px").click()
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.inline-flex:nth-child(2)"))
    )
    response=driver.find_element(By.CSS_SELECTOR,".js-article-content > div:nth-child(1) > div:nth-child(1)").text

    return response
def image_prompt(prompt,config):
    '''生成图像提示词'''
    image_prompts=config["image_prompt"]
    client = OpenAI(
    # 请用知识引擎原子能力API Key将下行替换为：api_key="sk-xxx",
    api_key=config["api_key"], # 如何获取API Key：https://cloud.tencent.com/document/product/1772/115970
    base_url=config["base_url"],
)
    completion = client.chat.completions.create(
        model=config['model'],  # 此处以 deepseek-r1 为例，可按需更换模型名称。
        messages=[
            {'role': 'system', 'content':image_prompts}
            , {'role': 'user', 'content': prompt}
            ]
)
    img_prompt=completion.choices[0].message.content
    return img_prompt
def get_image(prompt,i):
    '''生成图像'''
    with open("settings.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    url = config.get('images_base_url')+'/images/generations'
    model = config.get('images_model')
    api_key = config.get('images_api_key')

    if not url or not model or not api_key:
        raise ValueError("图像生成配置不完整，请在设置中配置图像模型相关参数")

    payload = {
        "model": model,
        "prompt": image_prompt(prompt,config),
        "seed": random.randint(0, 1000000)
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.request("POST", url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        image_url=response.json()["images"][0]["url"]   
        response = requests.get(image_url, timeout=30)
        file_path = os.path.abspath(os.path.join("AIpost/news/images/", str(i) + ".png"))
        print(file_path)

        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
        return file_path
    except requests.exceptions.RequestException as e:
        return "请求失败"

def job(tick_update):
    news_list = toutiao_hot()
    for topic in news_list[4::1]:
        try:
            toutiao_writer(topic=topic)
            time.sleep(tick_update)
        except Exception as e:
            print(e)
            continue
def toutiao_hot():
    date =time.strftime('%Y-%m-%d')
    print(date)
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_argument('--headless')
    options.add_argument(f'user-agent={UserAgent.random}')
    driver=webdriver.Firefox(options=options)
    url='https://rebang.today/?tab=toutiao'
    driver.get(url=url)
    wait=WebDriverWait(driver,2000)
    turn_page=wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,".space-x-1 > div:nth-child(1)"))
    )
    time.sleep(1)
    driver.execute_script("window.scrollBy(0, 2000);")
    time.sleep(1)
    news_list=[]
    news=driver.find_elements(By.XPATH,"/html/body/div[1]/div/div[2]/div[2]/main/div/div[2]/ul/li/div[2]/a/h2/p")
    for new in news:
        news_list.append(new.text)
    print(news_list)
    return news_list

    

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
def toutiao_writer(topic) -> str:
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    #options.add_argument('--headless')
    options.add_argument(f'user-agent={UserAgent.random}')
    driver=webdriver.Firefox(options=options)
    try:
        url='https://mp.toutiao.com/profile_v4/graphic/publish?from=toutiao_pc'
        driver.get(url=url)
        time.sleep(1)
        with open("cookies.json", "r", encoding="utf-8") as f:
             web_cookies = json.load(f)
        for cookie in web_cookies:
            driver.add_cookie(cookie)
        driver.get(url=url)
        wait = WebDriverWait(driver, 20)
        turn_page=wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".byte-textarea"))
        )
        turn_page.click()
        news=webpage_deepseek(query=f"任务：用生动有趣的中文写一篇有关{topic}的最新的新闻。要求：\n1.必须先在书名号内写好一个20字左右的中文标题。然后才用中文写1000字左右的具体段落，接下来的要求也主要围绕具体段落展开。\n2.为每个段落(除了标题)写一小段对段落的艺术性描述（40个字左右）并放在段落开头（不包括标题）的【】里面。\n3.标题与段落、段落之间都必须通过+++换行，段落总共可分为四到八段。", r1=True, websearch=False)

    # 去除标点前的数字，保留标点
        news = re.sub(r'(\d+)([。！？，；])', r'\2', news)
        print(news)
        #输出这篇新闻的标题
        title = news.split("+++")[0].replace("《","").replace("》","")
        driver.find_element(By.CSS_SELECTOR,".editor-title > textarea:nth-child(2)").send_keys(title)
        contents= news.split("+++")[1:]
        print(contents)
        for content in contents:
            try:
            #提取【和】中间的内容
                keyword = content.strip("\n").split("【")[1].split("】")[0]
                print(keyword)
                #pic_path=WebDriverManager().generate_image(query=keyword)
                pic_path = get_image(prompt=keyword, i=random.randint(0, 1000000))
                #pic_path=get_pixabay_images(api_key="47054162-b71e0d9aadb68e45d834827c7",query=keyword,per_page=10)
                driver.find_element(By.CSS_SELECTOR,".ProseMirror").send_keys(content.replace("【"+keyword+"】",""))
                #driver.find_element(By.CSS_SELECTOR,".ProseMirror").send_keys(pic_path)

                if  len(pic_path) > 6:
                    send_to_clipboard(pic_path)
                    time.sleep(1)
                    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                    os.remove(pic_path)
            except Exception as e:
                print(e)
                continue
        #driver.find_element(By.CSS_SELECTOR,".ProseMirror").send_keys(Keys.CONTROL + 'p')
        pre=driver.find_element(By.CSS_SELECTOR,".close-btn").click()
        wait = WebDriverWait(driver, 20)
        driver.execute_script("window.scrollBy(0, 2000);")
        time.sleep(1)
        #选择城市
        wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[3]/section/main/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/div"))).click()
        location=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,".byte-select-view-search > input:nth-child(1)")))
        location.send_keys("北京")
        location.send_keys(Keys.ENTER)
        #创作声明
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label.byte-checkbox:nth-child(3) > span:nth-child(2) > div:nth-child(1)"))).click()
        publich_buttton=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".byte-btn:nth-child(6)")))
        publich_buttton.click()
        time.sleep(5)
        release_buttton=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".byte-btn:nth-child(5)")))
        time.sleep(1)
        release_buttton.click()
        time.sleep(5)
        driver.quit()
    except Exception as e:
        print(e)
        #driver.quit()
if __name__ == '__main__':
    print("启动自动发文系统...")
    if not os.path.exists("settings.json"):
        with open("settings.json", "w",encoding="utf-8") as f:
            config = {
                "base_url": "https://api.siliconflow.cn/v1",
                "api_key": "sk-aardxirtqpsnhqvocoqblbiirgtoeqmlgldlrzrjondasxll",
                "model": "THUDM/glm-4-9b-chat",
                "images_base_url": "https://api.siliconflow.cn/v1",
                "images_api_key": "sk-aardxirtqpsnhqvocoqblbiirgtoeqmlgldlrzrjondasxll", 
                "images_model": "black-forest-labs/FLUX.1-schnell",
                "image_prompt": "请将用户的输入升华具有大师水准的准确且标准且丰富的的英文绘图提示词（100个英文单词左右），以便绘图模型能够完美绘制。"
            }

            json.dump(config, f,ensure_ascii=False,indent=4)
    get_coo=int(input("是否为初次登录登录或者登录过期需重新登录（登录限定时间为二十秒，请提前准备扫码），1为是，2为否：\n"))
    if get_coo==1:
        driver=webdriver.Firefox()
        url='https://mp.toutiao.com/profile_v4/graphic/publish?from=toutiao_pc'
        driver.get(url=url)
        time.sleep(20)
        cookies=driver.get_cookies()
        with open("cookies.json", "w",encoding="utf-8") as f:
            json.dump(cookies,f,ensure_ascii=False,indent=4)
            print("已完成登录，登录数据已保存")
        driver.quit()

    hours_num=int(input("请输入间隔多少小时执行一次：\n"))
    print("已设置执行间隔为：{}小时".format(hours_num))
    tick_update=int(input("请输入写每篇文章的间隔秒数："))
    print("已设置写每篇文章的间隔为：{}秒".format(tick_update))
    print("开始自动写公众号文章，您已经无需执行任何操作！")
    print("先自动运行一次....请稍后...")
    # 立即运行一次
    job(tick_update)
    # 设置每小时运行一次
    schedule.every(hours_num).hours.do(job)
    
    # 保持程序运行
    while True:
        schedule.run_pending()
        time.sleep(1)