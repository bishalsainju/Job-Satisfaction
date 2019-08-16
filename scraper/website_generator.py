import pandas as pd
import requests
import config.config as config


config = config.Config()
project_root = config.project_root
data_path = config.data_path

df = pd.read_csv('~/Downloads/Fortune1000.csv')
# df = pd.read_csv('~/Downloads/Fortune50.csv')
company_list = df['Company Name'].tolist()

lst = []
for company in company_list:
    company_name = company.strip().replace('&', '').replace(' ', '-').lower()
    # company_review_site = 'http://www.indeed.com/cmp/'+company_name+'/reviews'
    company_review_site = 'https://fortune.com/fortune500/2019/'+company_name
    request = requests.get(company_review_site)
    if request.status_code == 200:
        lst.append([company, company_name, company_review_site])
    else:
        print(company)

df_site = pd.DataFrame(lst, columns =['Company', 'Company_Name', 'Company_Review_Site'])
df_site.to_csv(data_path+'/scraper_data/review_site1000', index=False)