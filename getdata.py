# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


########################## 爬取题库并存储 ###############################
session = requests.session()

tikubhs = [8692, 10988, 10989, 10990, 10991, 10992, 10993, 10994, 10995]  # 每一类题库的编号
pages = [153, 77, 13, 18, 22, 27, 10, 39, 12]  # 每一个题库的题目页数

from pymongo import MongoClient
client = MongoClient()
db = client.shitiDB    # 数据库名 shitiDB

shiti_table = db.shitis    # 表名 shitis

for tikubh, page_range in zip(tikubhs, pages):
    for page in range(1, page_range+1):
        # 试题库URL
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

