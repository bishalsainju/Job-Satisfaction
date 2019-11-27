from bs4 import BeautifulSoup
import requests

import pandas as pd
import requests
import config.config as config


config = config.Config()
project_root = config.project_root
data_path = config.data_path

df = pd.read_csv(data_path +'/scraper_data/fortune_site50.csv')

lst = []
for index, row in df.iterrows():
    rank = (row["Rank"])
    company = row["Company"]
    fortune_site = row["Company_Review_Site"]
    page = requests.get(fortune_site)
    soup = BeautifulSoup(page.text, features='html.parser')
    stats = soup.findAll('td', class_='dataTable__value--3n5tL dataTable__valueAlignLeft--3uvNx')
    lst.append([rank, company, fortune_site, stats[0].div.text, stats[1].div.text, stats[4].div.text])

df_stat = pd.DataFrame(lst, columns =['Rank', 'Company_Name', 'Fortune_Site', "CEO", "CEO_Title", "HQ_Location"])
df_stat.to_csv(data_path+'/Fortune_1000/fortune50_hq.csv', index=False)






