from selenium import webdriver
import time
driver=webdriver.Firefox()
url="https://cp.kuaishou.com/creative/hot-spot"
driver.get(url=url)
#1先进行一次手动登录
time.sleep(20)
cookie=driver.get_cookies()
print(cookie)
time.sleep(5)
coo=cookie
for cookie in coo:
    # Fix: Ensure cookie has secure=True when SameSite=None
    if cookie.get('sameSite') == 'None':
        cookie['secure'] = True
    try:
        driver.add_cookie(cookie)
    except Exception as e:
        print(f"Failed to add cookie {cookie.get('name', '')}: {e}")
time.sleep(5)
driver.get(url=url)
