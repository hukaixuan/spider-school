# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os

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

# http://ids.qfnu.edu.cn/authserver/login?service=http%3A%2F%2F202.194.188.19%2Fcaslogin.jsp
# 			===>http://202.194.188.19/caslogin.jsp
# http://ids.qfnu.edu.cn/authserver/login?service=http%3A%2F%2Fmy.qfnu.edu.cn%2Flogin.portal
# 			===>http://my.qfnu.edu.cn/index.portal
resp = session.get("http://ids.qfnu.edu.cn/authserver/login?service=http%3A%2F%2F202.194.188.19%2Fcaslogin.jsp", headers=headers)
bsObj = BeautifulSoup(resp.text, "html.parser")		# 注意resp要带text
lt = bsObj.find('input', {'name':'lt'})['value']
execution = bsObj.find('input', {'name':'execution'})['value']
# print(resp.headers)


params = {
	'username': os.environ.get('STU_ID'),
	'password': os.environ.get('STU_PWD'),
	'lt': lt,
	'execution': execution,
	'_eventId': 'submit',
	'rmShown': '1'
}


resp = session.post("http://ids.qfnu.edu.cn/authserver/login?service=http%3A%2F%2F202.194.188.19%2Fcaslogin.jsp", data=params, headers=headers)

# resp = session.get('http://202.194.188.19/')
print(resp.text)
