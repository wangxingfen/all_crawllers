from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import pyautogui
from web_cookies import web_cookies
import time
import pyperclip
def paste_text_and_enter(text: str):
    # 将文字复制到剪贴板
    pyperclip.copy(text)
    # 短暂延迟确保复制完成
    time.sleep(0.1)
    # 执行粘贴操作 (Ctrl+V)
    pyautogui.hotkey('ctrl', 'v')
    # 短暂延迟
    time.sleep(0.1)
    # 按下回车键
    pyautogui.press('enter')
class WebDriverManager:
    def __init__(self):
        options = Options()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-infobars')
        options.add_argument(f'user-agent={UserAgent.random}')
        self.driver = webdriver.Firefox(options=options)
        
        url = "https://www.doubao.com/chat"
        self.driver.get(url=url)
        for cookie in web_cookies["doubao"]:
            self.driver.add_cookie(cookie)
        self.driver.get(url=url)
        
        self.wait = WebDriverWait(self.driver, 2000)

    def generate_prompt(self, pic_path,change):
        draw_page = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".semi-input-textarea"))
        )
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".icon-only-dxFfqQ").click()
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.popover-content-item-wrapper-QPOZLt:nth-child(9)"))
        ).click()
        #self.driver.find_element(By.CSS_SELECTOR, "div.popover-content-item-wrapper-QPOZLt:nth-child(9)").click()
        paste_text_and_enter(pic_path)
        
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#flow-end-msg-send"))
        )
        draw_page.send_keys(f"把该图片中的主人公和画风尽可能详细丰富地解析成英文提示词，并增加以下内容{change}的英文形式，然后合并输出。")
        self.driver.find_element(By.CSS_SELECTOR, "#flow-end-msg-send").click()
        
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.semi-button:nth-child(8)"))
        )
        response = self.driver.find_element(By.CSS_SELECTOR, ".auto-hide-last-sibling-br").text
        print(response)
        self.driver.close()
        return response

    def generate_image(self, query):
        draw_page = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".semi-input-textarea"))
        )
        draw_page.send_keys("@")
        
        input_page = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".semi-input"))
        )
        input_page.send_keys("图像生成")
        input_page.send_keys(Keys.RETURN)
        
        image_prompt_input = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".container-by63Kk"))
        )
        input = f'画一个{query}的图片'
        paste_text_and_enter(input)
        #self.driver.find_element(By.CSS_SELECTOR, "#flow-end-msg-send").click()
        
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.container-ShnbG7:nth-child(3)"))
        )
        time.sleep(5)
        
        images = self.driver.find_elements(By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div/div/div/div/div[1]/div/div[2]/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div/div/img")
        img_list=[img.get_attribute("src") for img in images]
        self.driver.close()

        return img_list
    
if  __name__ == "__main__":
    pic_path="C:\\Users\\wangxingfeng\\Pictures\\2.png"
    driver_manager = WebDriverManager()
    prompt_generator =driver_manager.generate_prompt(pic_path=pic_path,change="这只猫眯着眼睛在笑，手里拿着苹果。")
    print(prompt_generator)
    driver_manager = WebDriverManager()
    image_generator = driver_manager.generate_image(prompt_generator)
    print(image_generator)
