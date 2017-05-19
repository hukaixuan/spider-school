# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


########### 模拟登录 ##################################
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
# print(resp.headers)


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


resp = session.post("http://ids.qfnu.edu.cn/authserver/login?service=http%3A%2F%2F202.194.188.19%2Fcaslogin.jsp", data=params, headers=headers)
####################################################


########################## 爬取题库并存储 ###############################
tikubhs = [8692, 10988, 10989, 10990, 10991, 10992, 10993, 10994, 10995]  # 每一类题库的编号
pages = [153, 77, 13, 18, 22, 27, 10, 39, 12]  # 每一个题库的题目页数

from pymongo import MongoClient
client = MongoClient()
db = client.shitiDB    # 数据库名 shitiDB

shiti_table = db.shitis    # 表名 shitis

for tikubh, page_range in zip(tikubhs, pages):
    for page in range(1, page_range+1):
        url = "http://aqjy.qfnu.edu.cn/redir.php?catalog_id=6&cmd=learning&tikubh="+str(tikubh)+"&page="+str(page)
        resp = session.get(url)
        resp.encoding = 'gb2312'
        bsObj = BeautifulSoup(resp.text, "html.parser")
        shitis = bsObj.find_all('div', class_='shiti')
        daans = bsObj.find_all('span', style='color:#666666')
        values = []
        for timu_str, daan_str in zip(shitis, daans):
            shitibh = int(timu_str.h3.text[0:5])
            timu = timu_str.h3.text[6:]
            daan = daan_str.text[daan_str.text.find('标准答案')+5:].strip(' ）')
            d = {'shitibh':shitibh, 'tikubh':tikubh, 'timu':timu, 'daan':daan}
            values.append(d)
        new_result = shiti_table.insert_many(values)
        # print('Multiple posts: {0}'.format(new_result.inserted_ids))
####################################################################

