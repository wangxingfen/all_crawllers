from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time
import json
import os
from openai import OpenAI
def responser(prompt):
    '''生成角色提示词'''
    with open("settings.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    client = OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"]
    )
    
    messages = [
        {'role': 'system', 'content': "你现在请假扮一个虚幻引擎主题的up主和你的潜在客户进行简短且友好的聊天，并试图通过说明自己课程的优越性来将对方转化为自己的粉丝，千万不要暴露出你的ai身份。"},
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
def get_bilibili_info(query: str, max_results: int = 20) -> str:
    if not os.path.exists("users.json"):
        with open("users.json", "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=4)
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    #options.add_argument('--headless')
    options.add_argument(f'user-agent={UserAgent.random}')
    
    # 添加更多反反爬机制
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("dom.webnotifications.enabled", False)
    
    driver=webdriver.Firefox(options=options)
    url=f"https://search.bilibili.com/all?keyword={query}&order=dm"
    driver.get(url=url)
    with open("all_cookies.json", "r", encoding="utf-8") as f:
        web_cookies = json.load(f)
    for cookie in web_cookies["bilibili_msg"]:
        driver.add_cookie(cookie)
    driver.get(url=url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    href_list=[]
    contents=driver.find_elements(By.XPATH,"/html/body/div[3]/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/a")
    for content in contents:
        href=content.get_attribute("href")
        href_list.append(href)
    for href in href_list:
        #除掉最后一个字符
        add="?vd_source=64bb980e1cf0dcd46bf401f9ea5d4c74"
        driver.get(url=href+add)
        time.sleep(1)
        for i in range(1,3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        
        # 修改: 等待 bili-comments 元素加载完成
        try:
            # 等待 bili-comments 元素出现
            wait = WebDriverWait(driver, 10)
            comments_element = wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "bili-comments"))
            )
            
            # 确保自定义元素已完全加载
            driver.execute_script("""
                return new Promise(resolve => {
                    const element = document.querySelector('bili-comments');
                    if (element.shadowRoot) {
                        resolve(true);
                    } else {
                        // 等待 shadowRoot 出现
                        const observer = new MutationObserver(() => {
                            if (element.shadowRoot) {
                                observer.disconnect();
                                resolve(true);
                            }
                        });
                        observer.observe(element, { childList: true, subtree: true });
                        // 设置超时
                        setTimeout(() => {
                            observer.disconnect();
                            resolve(false);
                        }, 5000);
                    }
                });
            """)
            
            # 修改: 提取 bili-comments 中的用户信息和评论内容
            users_script = """
                const commentsElement = document.querySelector('bili-comments');
                if (!commentsElement || !commentsElement.shadowRoot) {
                    return [];
                }
                const shadowRoot = commentsElement.shadowRoot;
                
                // 查找评论线程项 - 按照新的选择器路径
                const commentThreads = shadowRoot.querySelectorAll('bili-comment-thread-renderer');
                const results = [];
                
                commentThreads.forEach(thread => {
                    try {
                        // 进入第一层 shadowRoot
                        if (!thread.shadowRoot) return;
                        
                        // 按照新路径查找 comment 元素
                        const commentItem = thread.shadowRoot.querySelector('#comment');
                        if (!commentItem || !commentItem.shadowRoot) return;
                        
                        // 进入第二层 shadowRoot
                        const commentShadow = commentItem.shadowRoot;
                        
                        // 按照新路径查找用户信息容器
                        const userInfoElement = commentShadow.querySelector('#header > bili-comment-user-info');
                        if (!userInfoElement || !userInfoElement.shadowRoot) return;
                        
                        // 进入第三层 shadowRoot
                        const userInfoShadow = userInfoElement.shadowRoot;
                        
                        // 按照新路径查找用户名链接
                        const userNameLink = userInfoShadow.querySelector('#user-name > a');
                        const userName = userNameLink ? userNameLink.textContent.trim() : '';
                        const userUrl = userNameLink ? userNameLink.href : '';
                        
                        // 获取评论内容
                        const richTextElement = commentShadow.querySelector('bili-rich-text');
                        let content = '';
                        if (richTextElement && richTextElement.shadowRoot) {
                            const richTextShadow = richTextElement.shadowRoot;
                            const contentElement = richTextShadow.querySelector('#contents');
                            content = contentElement ? contentElement.textContent.trim() : '';
                        }
                        
                        if (userName || content) {
                            results.push({
                                name: userName,
                                url: userUrl,
                                content: content
                            });
                        }
                    } catch (e) {
                        // 忽略单个评论项的错误
                        console.error('Error parsing comment thread:', e);
                    }
                });
                
                return results;
            """
            users_data = driver.execute_script(users_script)
            print(users_data)
            
            # 修改: 处理返回的数据并保存到文件
            if users_data:
                with open("users.json", "r", encoding="utf-8") as f:
                    existing_users = json.load(f)
                
                updated = False
                for user in users_data:
                    user_name = user['name']
                    user_url = user['url']
                    print(user_name, user_url)
                    if user_name not in existing_users:
                        existing_users[user_name] = user_url
                        updated = True
                
                if updated:
                    with open("users.json", "w", encoding="utf-8") as f:
                        json.dump(existing_users, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error processing comments: {e}")
            continue
    driver.quit()
def chat_with_users():
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    #options.add_argument('--headless')
    options.add_argument(f'user-agent={UserAgent.random}')
    
    # 添加更多反反爬机制
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("dom.webnotifications.enabled", False)
    
    driver=webdriver.Firefox(options=options)
    url=f"https://search.bilibili.com"
    driver.get(url=url)
    with open("all_cookies.json", "r", encoding="utf-8") as f:
        web_cookies = json.load(f)
    for cookie in web_cookies["bilibili_msg"]:
        driver.add_cookie(cookie)
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)
    # 修改: 创建 users 字典的副本以避免在迭代时修改原始字典
    for user_name, user_url in list(users.items()):
        try:
            driver.get(url=user_url)
            wait = WebDriverWait(driver, 20)
            wait.until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[2]/div/a'))
            ).click()
            #转到最新窗户
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
            wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div._MessageSendBox__ToolBtn_1izxa_13:nth-child(2)'))
            )
            piece="你好！"
            try:
                piece=responser(f"客户名：{user_name}，请开始打声招呼！")
                print(piece)
            except Exception as e:
                print(e)
            driver.find_element(By.CSS_SELECTOR, '.brt-editor').send_keys(piece)
            driver.find_element(By.CSS_SELECTOR, '._MessageSendBox__SendBtn_1izxa_69').click()
            #从列表中删除这个用户
            del users[user_name]
            with open("users.json", "w", encoding="utf-8") as f:
                json.dump(users, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error processing user: {e}")
        

if __name__ == '__main__':
    #print(get_bilibili_info("虚幻引擎"))
    chat_with_users()