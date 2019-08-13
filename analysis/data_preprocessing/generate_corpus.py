import pandas as pd
import config.config as config

config = config.Config()
project_root = config.project_root
data_path = config.data_path


def text_generator(satisfied_rating, df_company):
    texts = ""
    for r in satisfied_rating:
        text = "\n".join(review for review in df_company.loc[df_company.Rating_Number == r].Review_Text)
        texts = texts + "\n" + text
    return texts

def text_generator1(satisfied_rating, df_company):
    texts = ""
    for r in satisfied_rating:
        text = "\n".join(review for review in df_company.loc[df_company.Rating_Number == r].Review_Text)
        texts = texts + "\n" + text
    return texts


def append_corpus(company_rank, company_name, corpus_path, rating_list=range(1,6)):
    df_company = pd.read_csv(data_path + f'/companies/{company_rank}_{company_name}/{company_name}.csv')
    text = text_generator(rating_list, df_company)
    print(company_name)
    with open(corpus_path, mode='a+', encoding='utf8') as file:
        file.write(text)

def append_corpus1(company_rank, company_name, corpus_path, pro_con_text="pros"):
    df_company = pd.read_csv(data_path + f'/companies/{company_rank}_{company_name}/{company_name}.csv')
    text = text_generator(pro_con_text, df_company)
    with open(corpus_path, mode='a+', encoding='utf8') as file:
        file.write(text)


def append_corpus_overall(companies_list=range(1,51), satisfied_rating=[4, 5],\
                          unsatisfied_rating=[1, 2]):
    df_company_list = pd.read_csv(data_path + "/scraper_data/review_site.csv")
    for company_index in companies_list:
        company_name = df_company_list.iloc[company_index - 1]['Company_Name']
        # corpus_path = data_path + '/overall/overall_company_corpus'
        # append_corpus(company_rank=company_index, company_name=company_name,\
        #               corpus_path=corpus_path + ".txt", rating_list=range(1, 6))
        # append_corpus(company_rank=company_index, company_name=company_name,\
        #               corpus_path=corpus_path + "_satisfied.txt", rating_list=satisfied_rating)
        # append_corpus(company_rank=company_index, company_name=company_name,\
        #               corpus_path=corpus_path + "_unsatisfied.txt", rating_list=unsatisfied_rating)
        corpus_path = data_path + '/overall'
        append_corpus1(company_rank=company_index, company_name=company_name,
                      corpus_path=corpus_path+'/pros.csv', pro_con_text = "pros")
        append_corpus1(company_rank=company_index, company_name=company_name,
                      corpus_path=corpus_path + '/cons.csv', pro_con_text="cons")
        print(f'Appended texts from {company_index}. {company_name} to the corpus.')


if __name__ == '__main__':
    append_corpus_overall(companies_list=range(1, 51), satisfied_rating = [4, 5],\
                          unsatisfied_rating = [1, 2])
