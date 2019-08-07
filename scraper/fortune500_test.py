from bs4 import BeautifulSoup
import requests
import os
import time
import csv
import pandas as pd
import config.config as config


# page_str = 'https://fortune.com/fortune500/2019/univision-communications'
# page_str = 'https://fortune.com/fortune500/2019/univision-communications'
page_str = 'https://fortune.com/fortune500/2019/search/'



page = requests.get(page_str)

print(page.text)


soup = BeautifulSoup(page.text, features='html.parser')

print(soup)
#
# soups = soup.findAll('div', class_='container__xxl--3SCes container__container--a5NXK searchWrapper__wrapper--1MLSI container__padding--2mKn5')
# print(soups)
