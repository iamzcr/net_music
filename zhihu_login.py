#-*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
s = requests.session()
headers_base = { 
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
	'Accept-Encoding': 'gzip, deflate, sdch',
	'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2', 
	'Connection': 'keep-alive', 
	'Host': 'www.zhihu.com', 
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36', 
	'Referer': 'http://www.zhihu.com/', 
}
def login():
	url = 'http://www.zhihu.com'
	login_url = url+'/login/email'
	login_data = {
		'email': '1076686352@qq.com', 
		'password': '172839456a',
		'rememberme': 'true',
	}
	login_data['_xsrf'] = get_xsrf(url)
	res = s.post(login_url, headers=headers_base, data=login_data)
	login_cookies = None
	if(res.status_code == 200):
		login_cookies = res.cookies
	return login_cookies

def get_xsrf(url=None):
	r = s.get(url, headers=headers_base)        
	xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)', r.text)
	if xsrf == None:
		return ''
	else:
		return xsrf.group(0)
def get_users(my_cookie):
	test_url = 'https://www.zhihu.com/people/phpnao-can-fen/answers'
	headers_base = {
		'Accept' :'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Encoding' :	'gzip, deflate, br',
		'Accept-Language' :'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
		'Connection' :'keep-alive',
		'Host' :'www.zhihu.com',
		'Referer':'https://www.zhihu.com/people/phpnao-can-fen/answers',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
	}
	res = s.get(test_url, headers=headers_base, cookies=my_cookie,verify=False)
	users = re.search(r'<a title="*>', res.text)
	print users
if __name__ == '__main__':
	my_cookie = login()
	print my_cookie
	if my_cookie:
		get_users(my_cookie)
		

