# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient()
db = client.shitiDB    # 数据库名 shitiDB
table = db.shitis    # 表名 shitis

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

TEST_PAGE_NUM = 10      # 在线练习时页面数：1-10
KAOSHI_PAGE_NUM = 15    # 正式考试时页面数：1-15

###################### 模拟登录 ##########################
def login(username, password):
    """
    模拟登录，返回Session
    """
    session = requests.session()

    resp = session.get("http://ids.qfnu.edu.cn/authserver/login?service=http%3A%2F%2F202.194.188.19%2Fcaslogin.jsp", headers=headers)
    bsObj = BeautifulSoup(resp.text, "html.parser")     # 注意resp要带text
    lt = bsObj.find('input', {'name':'lt'})['value']
    execution = bsObj.find('input', {'name':'execution'})['value']


    params = {
        # 'username': os.environ.get('STU_ID'),
        # 'password': os.environ.get('STU_PWD'),
        'username': username,
        'password': password,
        'lt': lt,
        'execution': execution,
        '_eventId': 'submit',
        'rmShown': '1'
    }


    resp = session.post("http://ids.qfnu.edu.cn/authserver/login", data=params, headers=headers)
    
    resp = session.get("http://aqjy.qfnu.edu.cn/exam_tyrz_check.php")
    resp.encoding = 'gb2312'
    bsObj = BeautifulSoup(resp.text, "html.parser")
    name = bsObj.find('div', class_='explanation').text.strip().split('，')[0]
    print('登录成功, 欢迎您：%s'%name)
    print('#'*40)
    return session
########################################################


########################### 答题 #######################################
def post_per_page(session, page):   
    # 在线练习页面
    # url = "http://aqjy.qfnu.edu.cn/redir.php?catalog_id=6&cmd=dati&mode=test"   

    # 正式考试题页面
    url = "http://aqjy.qfnu.edu.cn/redir.php?catalog_id=6&cmd=dati"

    # 点击下一页页面提交数据：runpage一直为0，page从第一页无 到0 到页数-2，direction为1表示点击了下一页
    values = {}
    values['runpage'] = 0
    values['page'] = page
    values['direction'] = 1
    values['tijiao'] = 0
    values['postflag'] = 0
    values['autosubmit'] = 0
    # values['mode'] = 'test'   # 在线练习是 mode 设为 test

    if page == -1:         # 起始页处理
        # 在线练习页面
        resp = session.get('http://aqjy.qfnu.edu.cn/redir.php?catalog_id=6&tikubh=8692&cmd=testing')

        # 考试页面 --- 先获取答题按钮链接（每个院可能不同）
        # resp = session.get("http://aqjy.qfnu.edu.cn/redir.php?catalog_id=6")
        # bsObj = BeautifulSoup(resp.text, "html.parser")
        # link = bsObj.find('a',class_='zxks-bnt-green startKs')
        # link = 'http://aqjy.qfnu.edu.cn/'+str(link['href'])
        # resp = session.get(link)
    else:           # 其余页处理
        resp = session.post(url, data=values, headers=headers)

    resp.encoding = 'gb2312'
    bsObj = BeautifulSoup(resp.text, "html.parser")

    # 获取该页面试题
    shitis = bsObj.find_all('div', class_='shiti')

    for shiti in shitis:
        xuxuan = shiti.find('ul')
        shiti_text = shiti.h3.text
        split_index = shiti_text.find('、')
        shiti_id = 'ti_'+shiti_text[:split_index]
        shiti = shiti_text[split_index+1:].strip()
        print('%s.题目：%s'%(shiti_id, shiti), end='=====>>>>>')
        timu = table.find_one({'timu':shiti})
        daan = timu.get('daan').strip()
        if daan=='正确':
            daan='对'
        elif daan=='错误':
            daan='错'
        for daan_li in xuxuan.find_all('li'):
            daan_text = daan_li.text
            if daan in daan_text:
                values[shiti_id] = daan_li.input['value']
                print('答案：',daan_text)

    values['tijiao'] = 1 if page+2==TEST_PAGE_NUM else 0    # 在线练习时是否提交试题
    # values['tijiao'] = 1 if page+2==KAOSHI_PAGE_NUM else 0    # 正式考试时是否提交试题

    values['postflag'] = 1
    resp = session.post(url, data=values, headers=headers)
    print('#'*40)
    print('本次页面跳转提交的数据:',values)
    print('#'*40)
    resp.encoding = 'gb2312'
    return resp


def process(username, password ):
    session = login(username, password)
    for x in range(1, KAOSHI_PAGE_NUM):       # 正式考试
        res = post_per_page(session, x-2)
        if x+2 == KAOSHI_PAGE_NUM:
            return res.text

    # for x in range(1, TEST_PAGE_NUM+1):           # 在线练习
    #     res = post_per_page(session, x-2)           # x: 1 -> 10; 参数page: -1 -> 8
    #     if x == TEST_PAGE_NUM:
    #         bsObj = BeautifulSoup(res.text, "html.parser")
    #         return bsObj.find('div', class_="shuoming").text
#########################################################

if __name__ == '__main__':
    print(process(input('请输学号：'), input('请输入密码：')))







