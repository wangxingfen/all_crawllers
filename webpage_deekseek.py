from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time
def webpage_deepseek(query: str,r1:bool,websearch:bool) -> str:
    account="18179543659"#官网账号，手机号或者邮箱
    secret_key="15970582146abcde"#官网密码
    date =time.strftime('%Y-%m-%d')
    print(date)
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    #options.add_argument('--headless')
    options.add_argument(f'user-agent={UserAgent.random}')
    driver=webdriver.Firefox(options=options)
    url=f"https://chat.deepseek.com/"
    driver.get(url=url)
    wait = WebDriverWait(driver, 20)
    turn_page=wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ds-tab:nth-child(2)"))
    )
    turn_page.click()
    login_button=wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ds-button:nth-child(6)"))
    )
    driver.find_element(By.CSS_SELECTOR,"div.ds-form-item:nth-child(3) > div:nth-child(1) > div:nth-child(1) > input:nth-child(2)").send_keys(account)
    driver.find_element(By.CSS_SELECTOR,"div.ds-form-item:nth-child(4) > div:nth-child(1) > div:nth-child(1) > input:nth-child(2)").send_keys(secret_key)
    login_button.click()
    
    textarea = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//textarea"))
    )
    textarea.send_keys(query)
    if r1:
        driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[1]").click()
        if websearch:
            driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[2]").click()
        driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div[2]").click()
        button_xpath = "/html/body/div[1]/div/div/div[2]/div[3]/div/div[2]/div/div/div[3]/div[1]/div/div/div[2]/div[3]/div[2]"
        wait = WebDriverWait(driver, 1000)
        wait.until(
            lambda x: x.find_element(By.XPATH, button_xpath).get_attribute("aria-disabled") == "true"
        )
        reasoning_part=driver.find_element(By.CSS_SELECTOR,"._48edb25").text
        content_part=driver.find_element(By.CSS_SELECTOR,".ds-markdown").text
        feed_back=f"\n推理部分：\n{reasoning_part}\n内容部分：\n{content_part}"
    else:
        if websearch:
            driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[2]").click()
        driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div[2]").click()
        button_xpath = "/html/body/div[1]/div/div/div[2]/div[3]/div/div[2]/div/div/div[3]/div[1]/div/div/div[2]/div[3]/div[2]"
        wait = WebDriverWait(driver, 1000)
        wait.until(
            lambda x: x.find_element(By.XPATH, button_xpath).get_attribute("aria-disabled") == "true"
        )
        feed_back=driver.find_element(By.CSS_SELECTOR,".ds-markdown").text 
    print(feed_back)
    return feed_back
if __name__ == "__main__":
    webpage_deepseek("帮我找一下今天5-25号有什么科技新闻？",r1=False,websearch=False)