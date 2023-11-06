import requests
import json
import pandas as pd
from flask import Flask, render_template

from User import get_cookie_by_phone
app = Flask(__name__)

def order_create():
    headers = {
        'authority': 'buy.damai.cn',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://detail.damai.cn/',
        'accept-language': 'zh,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7'
    }
    params = {
        'exParams': json.dumps(ex_params),
        'buyParam': sku_info,
        'buyNow': 'true',
        'spm': 'a2oeg.project.projectinfo.dbuy'
    }

    response = self.session.get('https://buy.damai.cn/orderConfirm', headers=headers,
                                params=params, cookies=self.login_cookies)
    result = re.search('window.__INIT_DATA__[\s\S]*?};', response.text)
    self.login_cookies.update(self.session.cookies)


def get_ticket_message(mobile, product_id):

    login_cookies = get_cookie_by_phone(mobile)

    headers = {
        'authority': 'passport.damai.cn',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://passport.damai.cn/login?ru=https://passport.damai.cn/accountinfo/myinfo',
        'accept-language': 'zh,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7',
    }

    response = requests.get('https://detail.damai.cn/item.htm?spm=a2oeg.search_category.0.0.367128df9TjyhD&id=738468281081&clicktitle=周杰伦2023“嘉年华”世界巡回演唱会—上海站',
                            cookies=login_cookies)

    return_data = json.loads(response.text)

def get_ticket_list(mobile):

    login_cookies = get_cookie_by_phone(mobile)

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

    response = requests.get('https://search.damai.cn/searchajax.html?keyword=&cty=上海&ctl=演唱会&sctl=&tsg=0&st=&et=&order=1&pageSize=30&currPage=1&tn=',
                            headers=headers,
                            cookies=login_cookies)

    return_data = json.loads(response.text)
    ticket_list = return_data["pageData"]['resultData']

    data_List = []
    for ticket in ticket_list:
        data = {
            "名称":ticket['name'],
            "类型":ticket['categoryname'],
            "城市":ticket['cityname'],
            "演员":ticket['actors'],
            "价格":ticket['price'],
            "价格区间":ticket['price_str'],
            "状态":ticket['showstatus'],
            "演出时间":ticket['showtime']
        }
        data_List.append(data)
    df = pd.DataFrame(data_List)
    return df


@app.route('/')
def index():
    df = get_ticket_list("19821168252")
    # 将DataFrame数据转换为HTML表格
    table_html = df.to_html(classes='table table-striped')
    return render_template('index.html', table=table_html)


if __name__ == "__main__":
    phone = input("请输入手机号码: ")
    # app.run(debug=True)
