from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform
import os

def account_login(login_id=None, login_password=None):
    """
    登录大麦网

    :param login_id:
    :param login_password:
    :param login_type:  选择哪种方式进行登录
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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(account_login("18135765391"))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
