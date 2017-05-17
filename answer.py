# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

headers = {
    # 'Host': 'ids.qfnu.edu.cn',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Referer': 'http://202.194.188.19/menu/top.jsp',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'
}

session = requests.session()

resp = session.get("http://ids.qfnu.edu.cn/authserver/login?service=http%3A%2F%2F202.194.188.19%2Fcaslogin.jsp", headers=headers)
bsObj = BeautifulSoup(resp.text, "html.parser")     # 注意resp要带text
lt = bsObj.find('input', {'name':'lt'})['value']
execution = bsObj.find('input', {'name':'execution'})['value']


params = {
    # 'username': os.environ.get('STU_ID'),
    # 'password': os.environ.get('STU_PWD'),
    'username': input('请输入学号：'),
    'password': input('请输入密码：'),
    'lt': lt,
    'execution': execution,
    '_eventId': 'submit',
    'rmShown': '1'
}


# resp = session.post("http://ids.qfnu.edu.cn/authserver/login?service=http%3A%2F%2F202.194.188.19%2Fcaslogin.jsp", data=params, headers=headers)
resp = session.post("http://ids.qfnu.edu.cn/authserver/login", data=params, headers=headers)
resp = session.get("http://aqjy.qfnu.edu.cn/exam_tyrz_check.php")
# resp = session.get('http://aqjy.qfnu.edu.cn/exam_tyrz_check.php?ticket=ST-4830810-DCFO6O2s3inwIOZynH3L-1b6n-cas-1495022270849')

from pymongo import MongoClient
client = MongoClient()
db = client.shitiDB    # 数据库名 shitiDB
table = db.shitis    # 表名 shitis
# resp = session.get('http://aqjy.qfnu.edu.cn/exam_tyrz_check.php?ticket=ST-4830810-DCFO6O2s3inwIOZynH3L-1b6n-cas-1495022270849')

def post_per_page(runpage):   # -1 ~ 13
    # url = "http://aqjy.qfnu.edu.cn/redir.php?catalog_id=6&cmd=dati&mode=test"
    url = "http://aqjy.qfnu.edu.cn/redir.php?catalog_id=6&cmd=dati"
    # url = "http://aqjy.qfnu.edu.cn/redir.php?catalog_id=6&cmd=kaoshi_chushih&kaoshih=28423"
    # resp = session.get("http://aqjy.qfnu.edu.cn/redir.php?catalog_id=6&tikubh=8692&cmd=testing")
    values = {}
    values['runpage'] = 0
    values['page'] = runpage
    values['direction'] = 1
    values['tijiao'] = 0
    values['postflag'] = 0
    values['autosubmit'] = 0
    # values['mode'] = 'test'
    if runpage==-1:
        # resp = session.get('http://aqjy.qfnu.edu.cn/redir.php?catalog_id=6&tikubh=8692&cmd=testing')
        resp = session.get('http://aqjy.qfnu.edu.cn/redir.php?catalog_id=6&cmd=kaoshi_chushih&kaoshih=28423')
    else:
        resp = session.post(url, data=values, headers=headers)
    resp.encoding = 'gb2312'
    # print(resp.text)
    bsObj = BeautifulSoup(resp.text, "html.parser")
    shitis = bsObj.find_all('div', class_='shiti')
    for shiti in shitis:
        xuxuan = shiti.find('ul')
        shiti_text = shiti.h3.text
        split_index = shiti_text.find('、')
        shiti_id = 'ti_'+shiti_text[:split_index]
        shiti = shiti_text[split_index+1:].strip()
        # print('题目：',shiti)
        timu = table.find_one({'timu':shiti})
        daan = timu.get('daan').strip()
        if daan=='正确':
            daan='对'
        elif daan=='错误':
            daan='错'
        # print('答案：',daan)
        for daan_li in xuxuan.find_all('li'):
            daan_text = daan_li.text
            if daan in daan_text:
                values[shiti_id] = daan_li.input['value']
    values['tijiao'] = 1 if runpage==13 else 0
    values['postflag'] = 1
    resp = session.post(url, data=values, headers=headers)
    print(values)
    resp.encoding = 'gb2312'
    return resp


for x in range(-1, 14):
    res = post_per_page(x)
    if x==13:
        print(res.text)













