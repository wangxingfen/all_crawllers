from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import time
import requests
from bs4  import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
def get_toutiao_interact():
    date =time.strftime('%Y-%m-%d')
    print(date)
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    #options.add_argument('--headless')
    options.add_argument(f'user-agent={UserAgent.random}')
    driver=webdriver.Firefox(options=options)
    i=1
    url=f"https://www.toutiao.com/?is_new_connect=0&is_new_user=0"
    driver.get(url=url)
    with open("all_cookies.json", "r", encoding="utf-8") as f:
        web_cookies = json.load(f)
    for cookie in web_cookies["toutiao"]:
        driver.add_cookie(cookie)
    driver.get(url=url)
    wait=WebDriverWait(driver,10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.feed-m-nav:nth-child(1) > ul:nth-child(1) > li:nth-child(1) > div:nth-child(1) > div:nth-child(1)"))).click()
    for i in range(50):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
    #/html/body/div[1]/div/div[5]/div[1]/div/div/div/div[2]/div[203]/div/div[3]/div/div[1]/div[3]/button
    likes1=driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[5]/div[1]/div/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div[3]/button")
    likes2=driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[5]/div[1]/div/div/div/div[2]/div/div/div[3]/div/div[1]/div[3]/button")
    for like in likes1+ likes2:
        try: 
            # 添加重试机制处理ElementClickInterceptedException
            max_retries = 3
            retry_count = 0
            while retry_count < max_retries:
                try:
                    # Scroll element into view before clicking
                    # Wait until element is scrolled into view properly
                    driver.execute_script("""
                        arguments[0].scrollIntoView({block: 'center'});
                        window.scrollBy(0, -50); // Fine-tune if needed
                    """, like)
                    
                    # Wait for scrolling to stabilize by checking element position
                    previous_position = None
                    attempts = 0
                    max_scroll_wait = 5  # Maximum wait time in seconds
                    
                    while attempts < max_scroll_wait * 10:  # Check every 0.1 seconds
                        # Get element's current position
                        current_position = driver.execute_script("""
                            var rect = arguments[0].getBoundingClientRect();
                            return {
                                top: rect.top,
                                bottom: rect.bottom,
                                left: rect.left,
                                right: rect.right
                            };
                        """, like)
                        
                        # If position hasn't changed since last check, scrolling is complete
                        if previous_position == current_position:
                            break
                            
                        previous_position = current_position
                        time.sleep(0.1)
                        attempts += 1
                    
                    wait.until(EC.element_to_be_clickable(like)).click()
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        print(f"Failed to click element after {max_retries} attempts: {e}")
                        break
                    else:
                        print(f"Attempt {retry_count} failed: {e}. Retrying...")
                        time.sleep(1)
        except Exception as e:
            print(e)
    
if  __name__ == '__main__':
    print(get_toutiao_interact())
