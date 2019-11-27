from bs4 import BeautifulSoup
import requests
import os
import time
import csv
import pandas as pd
import config.config as config


config = config.Config()
# project_root = config.project_root
data_path = config.data_path

# Extremely simple logger, writes to file and console (if turned on)
class SimpleLogger(object):
    def __init__(self, filename, log_console=False, log_file=False):
        self.log_console = log_console
        self.log_file = log_file
        self.file = None
        if self.log_file:
            self.file = open(filename, 'w')

    def __del__(self):
        if self.log_file:
            self.file.close()

    def log(self, msg):
        if self.log_console:
            print(msg)
        if self.log_file:
            print(msg, file=self.file)

def check_value_exist(soup_div):
    if(soup_div != None):
        return soup_div.text
    else:
        return 'NaN'

def scrape_review(s):
    rating_number = check_value_exist(s.find('div', class_='cmp-ratingNumber'))
    review_title = check_value_exist(s.find('div', class_='cmp-review-title').span)
    reviewer_job_title_status = check_value_exist(s.find('span', class_='cmp-reviewer-job-title'))
    reviewer_job_title = reviewer_job_title_status[0 : reviewer_job_title_status.find("(")]
    reviewer_job_status = reviewer_job_title_status[reviewer_job_title_status.find("(")+1 : reviewer_job_title_status.find(")")]
    reviewer_job_location = check_value_exist(s.find('span', class_='cmp-reviewer-job-location'))
    reviewed_date = check_value_exist(s.find('span', class_='cmp-review-date-created'))
    review_text = check_value_exist(s.find('span', class_='cmp-review-text'))
    pros = check_value_exist(s.find('div', class_='cmp-review-pro-text'))
    cons = check_value_exist(s.find('div', class_='cmp-review-con-text'))
    rate_table = s.find('table', class_='cmp-ratings-expanded')
    trs = rate_table.find_all('tr')
    rate_dims = []
    for tr in trs:
        span = tr.find_all('span')
        rate_dims.append(float(span[0]['style'][7:-2]) / 20)

    return (rating_number, rate_dims[0], rate_dims[1], rate_dims[2], rate_dims[3], rate_dims[4],
            review_title, reviewer_job_title, reviewer_job_status, reviewer_job_location,
            reviewed_date,review_text, pros, cons)


def scrape_reviews(url_ext, logger, start_page):
    print('aa')
    page_str = url_ext + start_page
    page = requests.get(page_str, timeout=5)
    soup = BeautifulSoup(page.text, features='html.parser')

    # try:
    #     soup.raise_for_status()
    # except Exception as e:
    #     print(e)
    #     logger.log(e)
    #     return None

    soups = soup.findAll('div', class_='cmp-review-container')
    print('0')
    next = True
    next_link = start_page
    while(next):
        count = 0
        if(next_link == '?start=0'):
            start_index = 0
        else:
            start_index = 1
        for s in soups[start_index:]:
            count = count + 1
            yield scrape_review(s)
        logger.log('Read ' + str(count) + ' entries from page ' + next_link[next_link.find('?'):])
        next_link_div = soup.findAll('a', class_='cmp-Pagination-link cmp-Pagination-link--nav')
        for _ in next_link_div:
            if _.text == 'Next':
                next_link = _['href']
                next = True
                break;
            next = False

        if(next):
            # print(next_link)
            page_str = 'https://www.indeed.com' + next_link
            page = requests.get(page_str)
            soup = BeautifulSoup(page.text, features='html.parser')
            soups = soup.findAll('div', class_='cmp-review-container')


def store_the_reviews(filename, company_site, logger, start_page, start_index):
    start_total = time.time()
    i = start_index
    # We really don't want to overwrite any existing good DB file, it takes a long time to scrape all of the data
    if not os.path.exists(filename):
        with open(filename, 'w+', newline='') as file:
            print('a')
            csv_file = csv.writer(file)
            csv_file.writerow(['Index', 'Rating_Number', 'Work_Life', 'Benefits', 'Job_Advancement',
                               'Management', 'Culture', 'Review_Title', 'Reviewer_Job_Title',
                               'Reviewer_Job_Status', 'Reviewer_Job_Location',
                               'Reviewed_Date', 'Review_Text', 'Pros', 'Cons'])

    with open(filename, 'a', newline='') as file:
        print('b')
        csv_file = csv.writer(file)
        # csv_file.writerow(['Index', 'Rating_Number', 'Review_Title', 'Reviewer_Job_Title', 'Reviewer_Job_Status', 'Reviewer_Job_Location',
        #                    'Reviewed_Date', 'Review_Text'])
        start_row = time.time()
        for entry in scrape_reviews(company_site, logger, start_page):
            entry = (i,) + entry
            # print('d')
            csv_file.writerow(entry)
            # print('e')
            exec_time_row = time.time() - start_row
            # logger.log('In {:.3f} seconds - '.format(exec_time_row) + str(entry))
            start_row = time.time()
            i += 1
    exec_time_total = time.time() - start_total
    logger.log('{} total entries in {:.3f} seconds'.format(i - 1, exec_time_total))


def scrape_company(company, company_name, company_site, start_page, start_index):
    file_dir = path + '/' + company[:company.find('.')] + '_' + company_name
    filename = file_dir + '/' + company_name + '.csv'
    logger_name = file_dir + '/' + company_name + '_log.txt'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    logger = SimpleLogger(logger_name, True, True)
    store_the_reviews(filename, company_site, logger, start_page, start_index)


def scrape_companies(start_company_index, start_page, start_index):
    df = pd.read_csv(data_path + '/scraper_data/review_site.csv')
    logger_all = SimpleLogger('logs.txt', True, True)
    logger_all.log('Scraping for {}'.format(df.iloc[[start_company_index-1]]['Company'].values[0]))
    scrape_company(df.iloc[[start_company_index-1]]['Company'].values[0], \
                   df.iloc[[start_company_index-1]]['Company_Name'].values[0], \
                   df.iloc[[start_company_index-1]]['Company_Review_Site'].values[0],\
                   start_page, start_index)
    logger_all.log('Scraping for {} completed.'.format(df.iloc[[start_company_index-1]]['Company'].values[0]))
    # for index, row in df[start_company_index:].iterrows():
    #     start_page = '?start=0'
    #     company = row['Company']
    #     company_name = row['Company_Name']
    #     company_site = row['Company_Review_Site']
    #     logger_all.log('Scraping for {}'.format(company))
    #     scrape_company(company, company_name, company_site, start_page, 1)
    #     logger_all.log('Scraping for {} completed'.format(company))


if __name__ == '__main__':
    path = data_path + '/companies_updated'
    scrape_companies(start_company_index=1, start_page='?start=0', start_index=0)
    print("Commented")
