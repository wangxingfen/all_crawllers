from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from web_cookies import web_cookies
import time
def webpage_deepseek(query: str,r1:bool,websearch:bool) -> str:
    account=""#官网账号，手机号或者邮箱
    secret_key=""#官网密码
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
    
    #return feed_back
if __name__ == "__main__":
    webpage_deepseek("帮我找一下今天5-25号有什么科技新闻？",r1=True,websearch=False)