import pandas as pd
import requests
import config.config as config


config = config.Config()
project_root = config.project_root
data_path = config.data_path

df = pd.read_csv(data_path +'/scraper_data/Fortune1000.csv')

count = 0
lst = []
for index, row in df.iterrows():
    rank = int(row["Rank"])
    company = row["Company Name"]
    company_name = company.strip().replace('&', '').replace(' ', '-').lower()
    company_review_site = 'https://fortune.com/fortune500/2019/' + company_name
    request = requests.get(company_review_site)
    if request.status_code == 200:
        lst.append([rank, company, company_name, company_review_site])
    else:
        print(company)
    count += 1
    if(count == 50):
        break

df_site = pd.DataFrame(lst, columns =['Rank', 'Company', 'Company_Name', 'Company_Review_Site'])
df_site.to_csv(data_path+'/scraper_data/fortune_site50.csv', index=False)