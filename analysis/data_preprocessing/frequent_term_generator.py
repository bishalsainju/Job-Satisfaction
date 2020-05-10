import os
import pandas as pd
from analysis.data_preprocessing.preprocess import generate_ngrams
from analysis.data_preprocessing.generate_corpus import text_generator
import config.config as config


config = config.Config()
project_root = config.project_root
data_path = config.data_path


def frequency_generator(output_path, texts, n_gram, total_terms, satisfy_text):
    generate_ngrams(texts, n_gram, save_filename=output_path + f'/{n_gram}_gram_{satisfy_text}.txt',
                        read_percent=1, ngram_total=total_terms, count_store=True, sort=False, save_file=True)



def frequent_generator_companies(companies_list=range(1,51), path=project_root+'/data/companies',\
                            n_gram = 1, total_terms = 100, satisfied_rating = [4, 5],\
                                 unsatisfied_rating = [1, 2, 3] ):
    df_company_list = pd.read_csv(config.data_path + "/scraper_data/review_site.csv")
    for company_index in companies_list:
        company_name = df_company_list.iloc[company_index - 1]['Company_Name']
        company_data_path = path + f'/{company_index}_{company_name}/{company_name}.csv'
        output_path = path + f'/{company_index}_{company_name}/output_data/term_frequency'
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        df_company = pd.read_csv(company_data_path)
        frequency_generator(output_path, text_generator(satisfied_rating, df_company), n_gram, total_terms, "satisfied")
        frequency_generator(output_path, text_generator(unsatisfied_rating, df_company), n_gram, total_terms, "unsatisfied")
        print(f'Generated term frequency text for {company_index}. {company_name}')


if __name__ == '__main__':

    frequent_generator_companies(companies_list=[5], path=project_root+'/data/companies',\
                                n_gram = 1, total_terms = 500, satisfied_rating = [4, 5],\
                                     unsatisfied_rating = [1, 2])
    # corpus_satisfied = " ".join(open(project_root + '/data/overall/overall_company_corpus_satisfied.txt',
    #                                  mode='r', encoding='utf8').read().splitlines())
    # corpus_unsatisfied = " ".join(open(project_root + '/data/overall/overall_company_corpus_unsatisfied.txt',
    #                                    mode='r', encoding='utf8').read().splitlines())
    #
    # frequency_generator(output_path=project_root + '/data/overall/term_frequency', texts=corpus_satisfied,
    #                     n_gram=1, total_terms=500, satisfy_text="satisfied")
    # frequency_generator(output_path=project_root + '/data/overall/term_frequency', texts=corpus_unsatisfied,
    #                     n_gram=1, total_terms=500, satisfy_text="unsatisfied")
