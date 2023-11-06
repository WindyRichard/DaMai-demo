from Util import generate_response
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform
import os
import requests
from bs4 import BeautifulSoup


def account_login(login_id=None, login_password=None):
    """
    登录大麦网
    :param login_id:
    :return:
    """
    damai_title = '大麦网-全球演出赛事官方购票平台-100%正品、先付先抢、在线选座！'

    login_url = 'https://passport.damai.cn/login'
    option = webdriver.ChromeOptions()  # 默认Chrome浏览器
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=option)
    driver.set_page_load_timeout(60)
    driver.get(login_url)
    driver.switch_to.frame('alibaba-login-box')  # 切换内置frame，否则会找不到元素位置
    driver.find_element(By.XPATH, '//div[@class="login-tabs-tab" and contains(text(), "短信登录")]').click()
    driver.find_element(By.NAME, 'fm-sms-login-id').send_keys(login_id)
    # option.add_argument('headless')               # Chrome以后台模式进行，注释以进行调试
    # option.add_argument('window-size=1920x1080')  # 指定分辨率
    # option.add_argument('no-sandbox')             # 取消沙盒模式
    # option.add_argument('--disable-gpu')          # 禁用GPU加速
    # option.add_argument('disable-dev-shm-usage')  # 大量渲染时候写入/tmp而非/dev/shm


    wait = WebDriverWait(driver, 3600)  # 最多等待3600秒
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'fm-btn'))).click()
    WebDriverWait(driver, 180, 0.5).until(EC.title_contains(damai_title))
    login_cookies = {}
    if driver.title != damai_title:
        print('登录异常，请检查页面登录提示信息')
    for cookie in driver.get_cookies():
        login_cookies[cookie['name']] = cookie['value']
    return login_cookies


def mock_login(phone):
    # 这只是一个模拟登录功能。实际情况下，你需要检查数据库或其他后端系统。
    cookie = account_login(phone)
    login_info = generate_response(phone=phone, cookie=cookie)
    append_to_file(login_info, "UserMessage.json")

    return cookie


def check_login_status(login_cookies):
    """ 检测是否登录成功 """
    personal_title = '我的大麦-个人信息'

    headers = {
        'authority': 'passport.damai.cn',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://passport.damai.cn/login?ru=https://passport.damai.cn/accountinfo/myinfo',
        'accept-language': 'zh,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7',
    }

    response = requests.get('https://passport.damai.cn/accountinfo/myinfo',
                            headers=headers,
                            cookies=login_cookies)
    personal_info = BeautifulSoup(response.text, 'html.parser')
    print(personal_info)
    if personal_info.title.text == personal_title:
        return True
    else:
        return False


def append_to_file(data, filename):
    entries = []
    try:
        with open(filename, 'r') as file:
            entries = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    found = False
    for entry in entries:
        if entry['phone'] == data.get('phone'):
            entry['cookie'] = data.get('cookie')
            found = True
            break

    if not found:
        entries.append(data)
    with open(filename, "w") as file:
        json.dump(entries, file)


def get_cookie_by_phone(mobile):
    entries = []
    try:
        with open("UserMessage.json", 'r') as file:
            entries = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    for entry in entries:
        if entry['phone'] == mobile:
            return entry['cookie']


if __name__ == "__main__":
    phone = input("请输入手机号码: ")
    cookie = mock_login(phone)
    get_cookie_by_phone(phone)
    if cookie != "":
        print(check_login_status(cookie))
    else:
        print("请前往登录")
