from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import time
import random
import csv
import os
def random_action(driver):
    actions = [
        # 随机滚动
        lambda: driver.execute_script(f"window.scrollBy(0, {random.randint(-100, 100)});"),
        # 随机移动鼠标
        lambda: ActionChains(driver).move_by_offset(random.randint(-10, 10), random.randint(-10, 10)).perform(),
        # 随机暂停
        lambda: time.sleep(random.uniform(0.1, 0.5)),
        # 随机移动到页面某个元素
        lambda: ActionChains(driver).move_to_element(random.choice(driver.find_elements(By.TAG_NAME, "div"))).perform()
    ]
    try:
        random.choice(actions)()
    except:
        pass  # 忽略任何可能的错误
    return random_action
def parse_date(writer,big_list,fieldnames):
    zhihu_question = big_list[0]
    care_adding = big_list[2]
    care_sum_up = big_list[3]
    browser_adding = big_list[4]
    browser_sum_up = big_list[5]
    answer_adding = big_list[6]
    answer_sum_up = big_list[7]
    agree_adding = big_list[8]
    agree_sum_up = big_list[9]
    writer.writerow(
            {
                f'{fieldnames[0]}':f'{zhihu_question}',
                f'{fieldnames[1]}': f'{care_adding}',
                f'{fieldnames[2]}': f'{care_sum_up}',
                f'{fieldnames[3]}': f'{browser_adding}',
                f'{fieldnames[4]}': f'{browser_sum_up}',
                f'{fieldnames[5]}': f'{answer_adding}',
                f'{fieldnames[6]}': f'{answer_sum_up}',
                f'{fieldnames[7]}': f'{agree_adding}',
                f'{fieldnames[8]}': f'{agree_sum_up}'
            }
        )

def zhihu_catcher():
    #清洗数据
    date =time.strftime('%Y-%m-%d')
    print(date)
    options=Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_argument(f'user-agent={UserAgent.random}')
    #options.headless=True
    driver=webdriver.Firefox(options=options)
    url='https://www.zhihu.com/creator/hot-question/hot'
    driver.get(url=url)
    #登录（默认知乎）
    #driver.implicitly_wait(10)
    #微信登录
    #driver.find_element(By.XPATH,'/html/body/div[1]/div/main/div/div/div/div/div[2]/div/div[3]/span/button[1]').click()
    coo=[{'name': '_zap', 'value': '4923a83e-3c29-4132-8a10-52589485d5a9', 'path': '/', 'domain': '.zhihu.com', 'secure': False, 'httpOnly': False, 'expiry': 1782110275, 'sameSite': 'None'}, {'name': '_xsrf', 'value': 'ec7a28af-2778-4dcd-a292-6521744839a0', 'path': '/', 'domain': '.zhihu.com', 'secure': False, 'httpOnly': False, 'sameSite': 'None'}, {'name': 'HMACCOUNT', 'value': 'CD6A48DF72E8DAEC', 'path': '/', 'domain': '.zhihu.com', 'secure': False, 'httpOnly': False, 'sameSite': 'None'}, {'name': 'd_c0', 'value': 'KrJTKu6aeBqPTleB0hzMBbmidLTYCU5CbNg=|1747550276', 'path': '/', 'domain': '.zhihu.com', 'secure': False, 'httpOnly': False, 'expiry': 1782110276, 'sameSite': 'None'}, {'name': 'SESSIONID', 'value': 'vjK5CGs0yhWqL5nvdjxB2nmK5pUplsibkAlS4oTuZxa', 'path': '/', 'domain': 'www.zhihu.com', 'secure': False, 'httpOnly': False, 'sameSite': 'None'}, {'name': 'JOID', 'value': 'VV0SBU2xhvrGsrcBGJKSbktdLHoCxe6w8_DycCnJ7K-2_oNtbPUF0q-xtwIZPqwgSaHpPRY7DvLE2DFnY8L7vRA=', 'path': '/', 'domain': 'www.zhihu.com', 'secure': False, 'httpOnly': False, 'sameSite': 'None'}, {'name': 'osd', 'value': 'VlERB0yyivnEs7QNG5CTbUdeLnsBye2y8vP-cyvI76O1_IJuYPYH06y9tAAYPaAjS6DqMRU5D_HI2zNmYM74vxE=', 'path': '/', 'domain': 'www.zhihu.com', 'secure': False, 'httpOnly': False, 'sameSite': 'None'}, {'name': 'captcha_session_v2', 'value': '2|1:0|10:1747550276|18:captcha_session_v2|88:Qjhuak9GcW5GM0hQaWFuZmg4a25DR0N0bFF3UU5VVjk1d1UzSDUzbHlsRXUyR2Q1Qm5pTldremlPMlhNWWdwUQ==|a1ea17c0e17bf18febc0dfa27aeefce50a18660116bc2573056e064559c0fa79', 'path': '/', 'domain': '.zhihu.com', 'secure': False, 'httpOnly': True, 'expiry': 1750142276, 'sameSite': 'None'}, {'name': '__snaker__id', 'value': 'lY0faFzR7FFLXgEc', 'path': '/', 'domain': 'www.zhihu.com', 'secure': False, 'httpOnly': False, 'expiry': 1779086277, 'sameSite': 'None'}, {'name': 'gdxidpyhxdE', 'value': 'h6%2BvlEio9p1E2t%2B5ih2MBwK2xq26%2F2eyd46havf%2FPG33DMHZWUp4h2%2ByuNM7WXrbaJbghQjaXypLc1Z5LeV9fejO3wvclZDN0TqEGupN0q%2FKPVbbP9E%2BlnI2G%2B3kUgsL%2BPZ7YLHMXR1U5%2BU9Xp%2Fj1oipUTDjbu7xH9E1dHuVbGgG6DBM%3A1747551178838', 'path': '/', 'domain': 'www.zhihu.com', 'secure': False, 'httpOnly': False, 'expiry': 1750143178, 'sameSite': 'None'}, {'name': 'z_c0', 'value': '2|1:0|10:1747550279|4:z_c0|92:Mi4xSUdNRVNRQUFBQUFxc2xNcTdwcDRHaVlBQUFCZ0FsVk5SODRXYVFBRlJqbWNSX3ItRWNYUnpBcF9VV2s1Q2tYUEVR|7732a098dc33ef7c2f0e016d92f34213b6abba0bf7ef01d972ee91d6a47dcccd', 'path': '/', 'domain': '.zhihu.com', 'secure': True, 'httpOnly': True, 'expiry': 1763102278, 'sameSite': 'None'}, {'name': 'SUBMIT_0', 'value': '14f1909a-0152-4642-b92a-222029f17b3e', 'path': '/', 'domain': 'www.zhihu.com', 'secure': False, 'httpOnly': False, 'expiry': 1747552079, 'sameSite': 'None'}, {'name': 'Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49', 'value': '1747550276', 'path': '/', 'domain': '.zhihu.com', 'secure': False, 'httpOnly': False, 'expiry': 1779086280, 'sameSite': 'None'}, {'name': 'Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49', 'value': '1747550280', 'path': '/', 'domain': '.zhihu.com', 'secure': False, 'httpOnly': False, 'sameSite': 'None'}, {'name': 'BEC', 'value': '6c53268835aec2199978cd4b4f988f8c', 'path': '/', 'domain': 'www.zhihu.com', 'secure': False, 'httpOnly': False, 'expiry': 1747553880, 'sameSite': 'None'}]


    for cookie in coo:
        driver.add_cookie(cookie)
    time.sleep(5)
    spans=["hour","day","week"]
    for span in spans:
        url=f'https://www.zhihu.com/creator/hot-question/hot/0/{span}'
        driver.get(url=url)
        fold_path = f'知乎热点/知乎{date}{span}热点合集'
        if not os.path.exists(fold_path):
            os.makedirs(fold_path)
        fieldnames=['问题','关注增量','关注总量','浏览增量','浏览总量','回答增量','回答总量','赞同增量','赞同总量']
        #操作
        pages=driver.find_elements(By.XPATH,'/html/body/div[1]/div/main/div/div[2]/div/div/div[2]/div/a')
        for page in pages:
            page.click()
            time.sleep(random.randint(2, 3))
            filename = f'{fold_path}/{page.text.replace('/','')}.csv'
            with open(filename, 'w', newline='', encoding='utf-8') as csvFile:
                writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
                writer.writeheader()
                for i in range(25):
                    time.sleep(random.uniform(0.3,1))
                    driver.execute_script("window.scrollBy(0, {});".format(random.randint(1000, 2000)))
                contents = driver.find_elements(By.XPATH,
                                                '/html/body/div[1]/div/main/div/div[2]/div/div/div[4]/div/div[2]/div')
                
                for content in contents:
                    big_list = content.text.replace(' ', '').split('\n')
                    #print(big_list)
                    if len(big_list) > 2:
                        parse_date(writer=writer, big_list=big_list,fieldnames=fieldnames)
if __name__ == '__main__':
    coo=[{'name': '_zap', 'value': '4923a83e-3c29-4132-8a10-52589485d5a9', 'path': '/', 'domain': '.zhihu.com', 'secure': False, 'httpOnly': False, 'expiry': 1782110275, 'sameSite': 'None'}, {'name': '_xsrf', 'value': 'ec7a28af-2778-4dcd-a292-6521744839a0', 'path': '/', 'domain': '.zhihu.com', 'secure': False, 'httpOnly': False, 'sameSite': 'None'}, {'name': 'HMACCOUNT', 'value': 'CD6A48DF72E8DAEC', 'path': '/', 'domain': '.zhihu.com', 'secure': False, 'httpOnly': False, 'sameSite': 'None'}, {'name': 'd_c0', 'value': 'KrJTKu6aeBqPTleB0hzMBbmidLTYCU5CbNg=|1747550276', 'path': '/', 'domain': '.zhihu.com', 'secure': False, 'httpOnly': False, 'expiry': 1782110276, 'sameSite': 'None'}, {'name': 'SESSIONID', 'value': 'vjK5CGs0yhWqL5nvdjxB2nmK5pUplsibkAlS4oTuZxa', 'path': '/', 'domain': 'www.zhihu.com', 'secure': False, 'httpOnly': False, 'sameSite': 'None'}, {'name': 'JOID', 'value': 'VV0SBU2xhvrGsrcBGJKSbktdLHoCxe6w8_DycCnJ7K-2_oNtbPUF0q-xtwIZPqwgSaHpPRY7DvLE2DFnY8L7vRA=', 'path': '/', 'domain': 'www.zhihu.com', 'secure': False, 'httpOnly': False, 'sameSite': 'None'}, {'name': 'osd', 'value': 'VlERB0yyivnEs7QNG5CTbUdeLnsBye2y8vP-cyvI76O1_IJuYPYH06y9tAAYPaAjS6DqMRU5D_HI2zNmYM74vxE=', 'path': '/', 'domain': 'www.zhihu.com', 'secure': False, 'httpOnly': False, 'sameSite': 'None'}, {'name': 'captcha_session_v2', 'value': '2|1:0|10:1747550276|18:captcha_session_v2|88:Qjhuak9GcW5GM0hQaWFuZmg4a25DR0N0bFF3UU5VVjk1d1UzSDUzbHlsRXUyR2Q1Qm5pTldremlPMlhNWWdwUQ==|a1ea17c0e17bf18febc0dfa27aeefce50a18660116bc2573056e064559c0fa79', 'path': '/', 'domain': '.zhihu.com', 'secure': False, 'httpOnly': True, 'expiry': 1750142276, 'sameSite': 'None'}, {'name': '__snaker__id', 'value': 'lY0faFzR7FFLXgEc', 'path': '/', 'domain': 'www.zhihu.com', 'secure': False, 'httpOnly': False, 'expiry': 1779086277, 'sameSite': 'None'}, {'name': 'gdxidpyhxdE', 'value': 'h6%2BvlEio9p1E2t%2B5ih2MBwK2xq26%2F2eyd46havf%2FPG33DMHZWUp4h2%2ByuNM7WXrbaJbghQjaXypLc1Z5LeV9fejO3wvclZDN0TqEGupN0q%2FKPVbbP9E%2BlnI2G%2B3kUgsL%2BPZ7YLHMXR1U5%2BU9Xp%2Fj1oipUTDjbu7xH9E1dHuVbGgG6DBM%3A1747551178838', 'path': '/', 'domain': 'www.zhihu.com', 'secure': False, 'httpOnly': False, 'expiry': 1750143178, 'sameSite': 'None'}, {'name': 'z_c0', 'value': '2|1:0|10:1747550279|4:z_c0|92:Mi4xSUdNRVNRQUFBQUFxc2xNcTdwcDRHaVlBQUFCZ0FsVk5SODRXYVFBRlJqbWNSX3ItRWNYUnpBcF9VV2s1Q2tYUEVR|7732a098dc33ef7c2f0e016d92f34213b6abba0bf7ef01d972ee91d6a47dcccd', 'path': '/', 'domain': '.zhihu.com', 'secure': True, 'httpOnly': True, 'expiry': 1763102278, 'sameSite': 'None'}, {'name': 'SUBMIT_0', 'value': '14f1909a-0152-4642-b92a-222029f17b3e', 'path': '/', 'domain': 'www.zhihu.com', 'secure': False, 'httpOnly': False, 'expiry': 1747552079, 'sameSite': 'None'}, {'name': 'Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49', 'value': '1747550276', 'path': '/', 'domain': '.zhihu.com', 'secure': False, 'httpOnly': False, 'expiry': 1779086280, 'sameSite': 'None'}, {'name': 'Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49', 'value': '1747550280', 'path': '/', 'domain': '.zhihu.com', 'secure': False, 'httpOnly': False, 'sameSite': 'None'}, {'name': 'BEC', 'value': '6c53268835aec2199978cd4b4f988f8c', 'path': '/', 'domain': 'www.zhihu.com', 'secure': False, 'httpOnly': False, 'expiry': 1747553880, 'sameSite': 'None'}]
    zhihu_catcher()

