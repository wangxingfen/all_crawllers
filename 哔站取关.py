from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import time
import random
import json
from openai import OpenAI
from selenium.common.exceptions import NoSuchElementException
def responser(prompt):
    '''生成角色提示词'''
    with open("settings.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    client = OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"]
    )
    
    messages = [
        {'role': 'system', 'content': "你现在请假扮一个up主和用户进行友好的聊天，不要暴露出你的身份。"},
        {'role': 'user', 'content': prompt},
    ]
    
    completion = client.chat.completions.create(
        model=config['model'],
        messages=messages,
        temperature=config['temperature'],
        max_tokens=config['max_tokens'],
        frequency_penalty=config['frequency_penalty'],
        presence_penalty=config['presence_penalty'],
        top_p=config['top_p'],
        n=1,
    )
    
    piece = completion.choices[0].message.content
    return piece
def check_element_exists(driver,i):
    try:
        driver.find_element(By.CSS_SELECTOR, f'div._SessionItem_dnmx0_1:nth-child({i}) > div:nth-child(4)')
        return True
    except NoSuchElementException:
        #print(f"Element with CSS selector '{i}' not found.")
        return False
def bilibili_bot():
    date =time.strftime('%Y-%m-%d')
    print(date)
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    #options.add_argument('--headless')
    options.add_argument(f'user-agent={UserAgent.random}')
    driver=webdriver.Firefox(options=options)
    url=f"https://space.bilibili.com/3494362969278731/relation/follow?spm_id_from=333.1007.0.0"
    driver.get(url=url)
    with open("all_cookies.json", "r", encoding="utf-8") as f:
        web_cookies = json.load(f)
    for cookie in web_cookies["bilibili_msg"]:
        driver.add_cookie(cookie)
    driver.get(url=url)
    time.sleep(1)
    i=0
    scroll_container=driver.find_element(By.CSS_SELECTOR, 'html')
    driver.execute_script("arguments[0].scrollTop += 200;", scroll_container)
    followers=driver.find_elements(By.XPATH, f'//*[@id="app"]/main/div[1]/div[2]/section/div[2]/div/div/div/div[2]/div[1]/div/div/div')
    for follower in followers:
        if follower.text=="已关注":
            follower.click()
            time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="app"]/main/div[1]/div[2]/div[2]/div[1]/button[11]').click()
    time.sleep(1)
    while True:
        scroll_container=driver.find_element(By.CSS_SELECTOR, 'html')
        driver.execute_script("arguments[0].scrollTop += 200;", scroll_container)
        followers=driver.find_elements(By.XPATH, f'//*[@id="app"]/main/div[1]/div[2]/section/div[2]/div/div/div/div[2]/div[1]/div/div/div')
        for follower in followers:
            if follower.text=="已关注":
                follower.click()
                time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="app"]/main/div[1]/div[2]/div[2]/div[1]/button[11]').click()
        time.sleep(random.randint(1,2))
    
    
if __name__ == '__main__':
    #print(responser("你好"))
    bilibili_bot()