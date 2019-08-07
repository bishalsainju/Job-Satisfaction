import os
import pandas as pd
from analysis.data_preprocessing.preprocess import generate_ngrams, is_useful_ngram
import config.config as config


config = config.Config()
project_root = config.project_root
data_path = config.data_path
company_path = config.company_path

def df_filter(rating_list, df):
    sentences = []
    for r in rating_list:
        sentences.extend(df.loc[df.Rating_Number == r].Review_Text.tolist())
    return sentences

def df_filter_procons(df, procon_text = "pros"):
    if procon_text == "pros":
        return df.Pros.dropna().tolist()
    elif procon_text == "cons":
        return df.Cons.dropna().tolist()

def pxdata_generator(output_path, sentences):
    ngram_company = []
    # print(sentences[:3])
    texts = ' '.join(sentences)
    ngram_company.append(generate_ngrams(texts, ngram=1, ngram_total = 1000, sort=True))
    ngram_company.append(generate_ngrams(texts, ngram=2, ngram_total = 500, sort=True))
    ngram_company.append(generate_ngrams(texts, ngram=3, ngram_total = 300, sort=True))
    processed_sentences = []
    ngram_company[0] = [x for x in ngram_company[0] if not any(c.isdigit() for c in x)]
    ngram_company[1] = [x for x in ngram_company[1] if not any(c.isdigit() for c in x[0])]
    # print(ngram_company[0])
    # print(len(ngram_company[0]))
    # print(ngram_company[1])
    # print(len(ngram_company[1]))
    # print(ngram_company[2])
    # print(len(ngram_company[2]))
    count=0
    # print(len(sentences))
    for sentence in sentences:
        n_grams_list = []
        n_grams_list.append(sentence)
        for ngram in range(1, 4):
            n_grams = generate_ngrams(sentence, ngram=ngram, sort=True)
            n_grams = [n_gram for n_gram in n_grams if is_useful_ngram(ngram_company[ngram-1],
                                                                       n_gram)]
            n_grams_string = ' '.join(n_grams)
            n_grams_list.append(n_grams_string)
        processed_sentences.append(n_grams_list)
        count += 1
        # print(count)

    df = pd.DataFrame.from_records(processed_sentences)
    df.columns = ['Review_Text', 'Unigrams', 'Bigrams', 'Trigrams']

    df.to_csv(output_path, encoding='utf-8')
    return processed_sentences


def pxdata_generator_companies(companies_list=range(1,51), path=company_path,
                            satisfied_rating = [4, 5], unsatisfied_rating = [1, 2],
                               rating_procon_text = 'rating'):

    df_company_list = pd.read_csv(config.data_path + "/scraper_data/review_site.csv")
    for company_index in companies_list:
        company_name = df_company_list.iloc[company_index - 1]['Company_Name']
        company_data_path = path + f'/{company_index}_{company_name}/{company_name}.csv'
        output_path = path + f'/{company_index}_{company_name}/output_data/px_data1'
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        df_company = pd.read_csv(company_data_path)
        if(rating_procon_text=='rating'):
            pxdata_generator(output_path+'/satisfied.csv', df_filter(satisfied_rating, df_company))
            pxdata_generator(output_path+'/unsatisfied.csv', df_filter(unsatisfied_rating, df_company))
            print(f'Generated px data for {company_index}. {company_name}')
        elif(rating_procon_text=='procon'):
            pxdata_generator(output_path + '/pros.csv', df_filter_procons(df_company, procon_text="pros"))
            pxdata_generator(output_path + '/cons.csv', df_filter_procons(df_company, procon_text="cons"))
            print(f'Generated px data for {company_index}. {company_name}')

if __name__ == '__main__':
    pxdata_generator_companies(companies_list=range(1, 51), rating_procon_text='procon')