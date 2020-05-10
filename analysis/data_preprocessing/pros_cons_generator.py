import os
import pandas as pd
from analysis.data_preprocessing.frequent_term_generator import frequency_generator
import config.config as config

config = config.Config()
project_root = config.project_root

def text_generator(df):
    texts = "\n".join(text for text in df["Texts"])
    return texts

def proscons_generator_companies(companies_list=range(1,51), path=project_root+'/data/companies',\
                            n_gram = 1, total_terms = 100):
    df_company_list = pd.read_csv(config.data_path + "/scraper_data/indeed_site50.csv")
    for company_index in companies_list:
        company_name = df_company_list.iloc[company_index - 1]['Company_Name']
        company_data_path = path + f'/{company_index}_{company_name}/{company_name}.csv'
        output_path = path + f'/{company_index}_{company_name}/output_data/pros_cons'
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        df_company = pd.read_csv(company_data_path)
        pros = df_company[['Pros']]
        pros = pros.rename(columns={'Pros': 'Texts'})
        pros = pros.dropna()
        cons = df_company[['Cons']]
        cons = cons.rename(columns={'Cons': 'Texts'})
        cons = cons.dropna()
        frequency_generator(output_path, text_generator(pros), n_gram, total_terms, "Pros")
        frequency_generator(output_path, text_generator(cons), n_gram, total_terms, "Cons")
        print(f'Generated pros_cons frequency text for {company_index}. {company_name}')


def reviews_generator_companies(companies_list=range(1,51), path=project_root+'/data/companies',\
                            n_gram = 1, total_terms = 100):
    df_company_list = pd.read_csv(config.data_path + "/scraper_data/indeed_site50.csv")
    for company_index in companies_list:
        company_name = df_company_list.iloc[company_index - 1]['Company_Name']
        company_data_path = path + f'/{company_index}_{company_name}/{company_name}.csv'
        output_path = path + f'/{company_index}_{company_name}/output_data/reviews'
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        df_company = pd.read_csv(company_data_path)
        reviews = df_company[['Review_Text']]
        reviews = reviews.rename(columns={'Review_Text': 'Texts'})
        reviews = reviews.dropna()
        frequency_generator(output_path, text_generator(reviews), n_gram, total_terms, "Reviews")
        print(f'Generated review text frequency text for {company_index}. {company_name}')


if __name__ == '__main__':

    reviews_generator_companies(companies_list=range(1, 5), path=project_root+'/data/companies',
                                n_gram=3, total_terms=300)