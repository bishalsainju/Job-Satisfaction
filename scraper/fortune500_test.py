# from bs4 import BeautifulSoup
# import requests
#
#
# page_str = 'https://fortune.com/fortune500/2019/univision-communications'
# # page_str = 'https://fortune.com/fortune500/2019/search/'
#
# page = requests.get(page_str)
# soup = BeautifulSoup(page.text, features='html.parser')
#
# print(soup)
# data = soup.findAll('div', class_='container__xxl--3SCes container__container--a5NXK searchWrapper__wrapper--1MLSI container__padding--2mKn5')
# print(data)


import json
import re
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from bs4 import BeautifulSoup

data = urllib2.urlopen('http://fortune.com/fortune500/')
soup = BeautifulSoup(data)
postid = next(attr for attr in soup.body['class'] if attr.startswith('postid'))
postid = re.match(r'postid-(\d+)', postid).group(1)

url = "http://fortune.com/data/franchise-list/{postid}/1/".format(postid=postid)
data = json.load(urllib2.urlopen(url))

resulting_url = urllib2.parse.urljoin(url, data['articles'][0]['url'])
print(resulting_url)