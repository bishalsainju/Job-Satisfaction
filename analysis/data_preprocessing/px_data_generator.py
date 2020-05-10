import os
import pandas as pd
from analysis.data_preprocessing.preprocess import generate_ngrams, is_useful_ngram
import config.config as config
config = config.Config()
company_path = config.company_path

def df_filter(rating_list, df):
    df_new = df[["Review_Text", "Rating_Number", "Reviewer_Job_Status", 'Reviewed_Year',
                     'Work_Life', 'Benefits', 'Job_Advancement', 'Management', 'Culture']]
    df_new = df_new.dropna()
    df_new.loc[df_new['Reviewer_Job_Status'] == 'Former Employee', 'Reviewer_Job_Status'] = 0
    df_new.loc[df_new['Reviewer_Job_Status'] == 'Current Employee', 'Reviewer_Job_Status'] = 1
    df_new.rename(columns={"Pros": "Review_Text"}, inplace=True)
    return df_new

def df_filter_procons(df, procon_text = "pros"):
    df_new = pd.DataFrame()
    if procon_text == "pros":
        df_new = df[["Pros", "Rating_Number", "Reviewer_Job_Status", 'Reviewed_Year',
                     'Work_Life', 'Benefits', 'Job_Advancement', 'Management', 'Culture']]
        df_new = df_new.dropna()
        df_new.loc[df_new['Reviewer_Job_Status'] == 'Former Employee', 'Reviewer_Job_Status'] = 0
        df_new.loc[df_new['Reviewer_Job_Status'] == 'Current Employee', 'Reviewer_Job_Status'] = 1
        df_new.rename(columns={"Pros": "Review_Text"}, inplace=True)
        return df_new
    elif procon_text == "cons":
        df_new = df[["Cons", "Rating_Number", "Reviewer_Job_Status", 'Reviewed_Year',
                     'Work_Life', 'Benefits', 'Job_Advancement', 'Management', 'Culture'
                     ]]
        df_new = df_new.dropna()
        sdf_new = df_new.dropna()
        df_new.loc[df_new['Reviewer_Job_Status'] == 'Former Employee', 'Reviewer_Job_Status'] = 0
        df_new.loc[df_new['Reviewer_Job_Status'] == 'Current Employee', 'Reviewer_Job_Status'] = 1
        df_new.rename(columns={"Cons": "Review_Text"}, inplace=True)
        return df_new

def pxdata_generator(output_path, df_filtered):
    ngram_company = []
    # print(sentences[:3])
    # print(df_filtered.head())
    sentences = df_filtered.Review_Text.tolist()
    ratings = df_filtered.Rating_Number.tolist()
    job_status = df_filtered.Reviewer_Job_Status.tolist()
    reviewed_year = df_filtered.Reviewed_Year.tolist()
    work_life = df_filtered.Work_Life.tolist()
    benefits = df_filtered.Benefits.tolist()
    job_advancement = df_filtered.Job_Advancement.tolist()
    management = df_filtered.Management.tolist()
    culture = df_filtered.Culture.tolist()
    # print(sentences)
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
        n_grams_list.append(ratings[count])
        n_grams_list.append(job_status[count])
        n_grams_list.append(reviewed_year[count])
        n_grams_list.append(sentence)
        for ngram in range(1, 4):
            n_grams = generate_ngrams(sentence, ngram=ngram, sort=True)
            n_grams = [n_gram for n_gram in n_grams if is_useful_ngram(ngram_company[ngram-1],
                                                                       n_gram)]
            n_grams_string = ' '.join(n_grams)
            n_grams_list.append(n_grams_string)
        n_grams_list.append(work_life[count])
        n_grams_list.append(benefits[count])
        n_grams_list.append(job_advancement[count])
        n_grams_list.append(management[count])
        n_grams_list.append(culture[count])
        processed_sentences.append(n_grams_list)
        count += 1
        # print(count)

    df = pd.DataFrame.from_records(processed_sentences)
    df.columns = ['Ratings', 'Job_Status', 'Reviewed_Year', 'Review_Text', 'Unigrams',
                  'Bigrams', 'Trigrams', 'Work_Life', 'Benefits', 'Job_Advancement',
                  'Management', 'Culture']

    df.to_csv(output_path, encoding='utf-8')
    return processed_sentences


def pxdata_generator_companies(companies_list=range(1,51), path=company_path,
                            rating = [1, 2, 3, 4, 5],
                               rating_procon_text = 'rating'):

    df_company_list = pd.read_csv(config.data_path + "/scraper_data/indeed_site50.csv")
    for company_index in companies_list:
        company_name = df_company_list.iloc[company_index - 1]['Company_Name']
        company_data_path = path + f'/{company_index}_{company_name}/{company_name}.csv'
        output_path = path + f'/{company_index}_{company_name}/output_data/px_data_reviews1'
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        df_company = pd.read_csv(company_data_path)
        if(rating_procon_text=='rating'):
            df_former = df_company[df_company.Reviewer_Job_Status == 'Former Employee']
            df_current = df_company[df_company.Reviewer_Job_Status == 'Current Employee']
            df_fc = pd.concat([df_former, df_current], ignore_index=True)
            # pxdata_generator(output_path+'/satisfied.csv', df_filter(satisfied_rating, df_company))
            # pxdata_generator(output_path+'/unsatisfied.csv', df_filter(unsatisfied_rating, df_company))
            pxdata_generator(output_path+'/reviews.csv', df_filter(rating, df_fc))
            print(f'Generated px data for {company_index}. {company_name}')
        elif(rating_procon_text=='procon'):
            df_former = df_company[df_company.Reviewer_Job_Status == 'Former Employee']
            df_current = df_company[df_company.Reviewer_Job_Status == 'Current Employee']
            df_fc = pd.concat([df_former, df_current], ignore_index=True)
            pxdata_generator(output_path + '/pros.csv', df_filter_procons(df_fc, procon_text="pros"))
            pxdata_generator(output_path + '/cons.csv', df_filter_procons(df_fc, procon_text="cons"))
            print(f'Generated px data for {company_index}. {company_name}')

if __name__ == '__main__':
    # pxdata_generator_companies(companies_list=range(1,51), rating_procon_text='procon')
    pxdata_generator_companies(companies_list=range(1, 51), rating_procon_text='rating')