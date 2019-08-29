import pandas as pd
import numpy as np

df_company_list = pd.read_csv('~/Desktop/workspace/indeed/Job-Satisfaction/data/scraper_data/review_site.csv')

for index, company in  df_company_list.iterrows():
    file_path = f'~/Desktop/workspace/indeed/Job-Satisfaction/data/companies/{index+1}_{company.Company_Name}/{company.Company_Name}.csv'
    df = pd.read_csv(file_path)
    df['Reviewed_Date'] = pd.to_datetime(df['Reviewed_Date'])
    df['Reviewed_Year'] = df['Reviewed_Date'].dt.year
    df.to_csv(file_path)
    print(company.Company_Name)

