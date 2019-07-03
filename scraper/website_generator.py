import pandas as pd
import requests

df = pd.read_csv('~/Downloads/Fortune50.csv')
company_list = df['Company'].tolist()

lst = []
for company in company_list:
    company_name = company[company.find('.')+2:].strip().replace(' ', '-')
    company_review_site = 'http://www.indeed.com/cmp/'+company_name+'/reviews'
    request = requests.get(company_review_site)
    if request.status_code == 200:
        lst.append([company, company_name, company_review_site])
    else:
        print(company)

df_site = pd.DataFrame(lst, columns =['Company', 'Company_Name', 'Company_Review_Site'])
df_site.to_csv('review_site.csv', index=False)