from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import Byt
import time
import random
import json
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def bilibili_like():
    date =time.strftime('%Y-%m-%d')
    print(date)
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_argument('--headless')
    driver=webdriver.Firefox(options=options)
    url=f"https://t.bilibili.com/?spm_id_from=333.1007.0.0"
    driver.get(url=url)
    with open("all_cookies.json", "r", encoding="utf-8") as f:
        web_cookies = json.load(f)
    for cookie in web_cookies["bilibili_msg"]:
        driver.add_cookie(cookie)
    driver.get(url=url)
    # 等待页面完全加载
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    time.sleep(1)

    # 使用JavaScript滚动具体元素
    for i in range(1,50):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
    wait=WebDriverWait(driver, 10)
    likes=driver.find_elements(By.XPATH, '/html/body/div[2]/div[3]/main/section[3]/div[2]/div[1]/div/div/div/div[4]/div[3]/div')
    for like in likes:
        try: 
            # Check if the element has the correct class attribute before clicking
            class_attribute = like.get_attribute("class")
            if class_attribute != "bili-dyn-action like":
                continue  # Skip this element if it doesn't have the correct class
            
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
                        time.sleep(0.5)
                        attempts += 1
                    
                    wait.until(EC.element_to_be_clickable(like)).click()
                    print(f"点赞成功{random.randint(1, 10)}")
                    time.sleep(1)
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
            print(f"Error clicking element: {e}")
def bilibili_like_reccommend():
    date =time.strftime('%Y-%m-%d')
    print(date)
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    #options.add_argument('--headless')
    driver=webdriver.Firefox(options=options)
    url=f"https://search.bilibili.com/all?keyword=%E6%B8%B8%E6%88%8F&order=pubdate"
    driver.get(url=url)
    with open("all_cookies.json", "r", encoding="utf-8") as f:
        web_cookies = json.load(f)
    for cookie in web_cookies["bilibili_msg"]:
        driver.add_cookie(cookie)
    driver.get(url=url)
    # 等待主页面加载完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    time.sleep(1)

    while True:
        for i in range(1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
        #/html/body/div/div/main/div/div[2]/div[2]/div[32]/div/div/div[2]/div[1]/a
        likes_urls=driver.find_elements(By.XPATH, '/html/body/div[3]/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div/a/h3')
        # Store the original window handle
        original_window = driver.current_window_handle
        for like_url in likes_urls:
            wait=WebDriverWait(driver, 10)
            try:
                # Check if driver session is still valid
                driver.title  # This will throw an exception if session is invalid
            except:
                print("WebDriver session is no longer valid")
                break
                
            # Switch back to original window before processing each element
            try:
                driver.switch_to.window(original_window)
            except:
                print("Cannot switch to original window, creating new session")
                break
                
            #if len(like_url.get_attribute("href"))>100:
             #   continue
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
                        """, like_url)
                        
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
                            """, like_url)
                            
                            # If position hasn't changed since last check, scrolling is complete
                            if previous_position == current_position:
                                break
                                
                            previous_position = current_position
                            attempts += 1
                        
                        wait.until(EC.element_to_be_clickable(like_url)).click()
                        break
                    except Exception as e:
                        retry_count += 1
                        if retry_count >= max_retries:
                            print(f"Failed to click element after {max_retries} attempts: {e}")
                            break
                        else:
                            print(f"Attempt {retry_count} failed: {e}. Retrying...")
                            break               
                # Check if new window was opened
                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[-1])
                    try:
                        # 等待视频页面加载完成
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '#arc_toolbar_report > div.video-toolbar-left > div > div:nth-child(1) > div'))
                        )
                        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#arc_toolbar_report > div.video-toolbar-left > div > div:nth-child(1) > div')))
                        like=driver.find_element(By.CSS_SELECTOR, '#arc_toolbar_report > div.video-toolbar-left > div > div:nth-child(1) > div')
                        if like.get_attribute("class")=="video-like video-toolbar-left-item":
                            like.click()
                            print(f"点赞成功{random.randint(1, 10)}")
                    except Exception as e:
                        print(e)
                    time.sleep(0.5)

                    driver.close()
                    # Switch back to the original window
                    try:
                        driver.switch_to.window(original_window)
                    except Exception as e:
                        print(f"Error switching back to original window: {e}")
                        break
  
            except Exception as e:
                print(e)
        
        # 等待页面刷新完成
        driver.refresh()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
if __name__ == '__main__':

    bilibili_like_reccommend()