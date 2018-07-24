import os
import re
import json
from pathlib import Path

from lxml import html
import pandas as pd
import langdetect as ld

ROOT_SAVE_DIR = r'C:\Users\rmdelgad\Documents\Berkeley MIDS\W266 Natural Language Processing\Final Project\Glassdoor\raw_data'
PARSED_DATA_DIR = r'C:\Users\rmdelgad\Documents\Berkeley MIDS\W266 Natural Language Processing\Final Project\Glassdoor\parsed_data'
TODAY = '2018-07-13'


def batch(iterable, n=1):
    '''Utility function for splitting an iterable into an iterable of smaller batches'''
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def parse_glassdoor_file(glassdoor_filename):
    '''Function to parse the file containing the scrape information into a pandas DataFrame.'''
    # Read in the
    with open(glassdoor_filename, 'r') as f:
        scrape_dict = json.load(f)

    # Read the page into an lxml etree. Remove line breaks from
    # the page as they mess up Pros/Cons parsing
    page = re.sub(r'<br ?/>', '', scrape_dict['body'])
    tree = html.fromstring(page)

    # Parse out the number of Helpful votes for each review
    helpful = tree.xpath('//span[text()="Helpful"]')
    hcounts_xpath = './/span[@class="count"]/span/text()'
    counts = [int(h.xpath(hcounts_xpath)[0]) if (h.xpath(hcounts_xpath)) else 0 for h in helpful]

    # Parse out rest of contents and store in a dictionary
    LI_REV_PREFIX = '//li[contains(@id,"empReview") and .//time]'
    parse_dict = {
        'Pros': tree.xpath(
            f'{LI_REV_PREFIX}//p[contains(@class,"pros mainText") and not(contains(@class,"hidden"))]/text()'),
        'Cons': tree.xpath(
            f'{LI_REV_PREFIX}//p[contains(@class,"cons mainText") and not(contains(@class,"hidden"))]/text()'),
        'Date': tree.xpath(f'{LI_REV_PREFIX}//time[@class="date subtle small"]/@datetime'),
        'Rating': tree.xpath('//span[@class="gdStars gdRatings sm margRt"]//span[@class="value-title"]/@title'),
        'Helpful': counts

    }
    parse_frame = pd.DataFrame(parse_dict)

    # Add in 'audit trail' fields
    parse_frame['Company'] = scrape_dict['company_name']
    parse_frame['Url'] = scrape_dict['url']
    parse_frame['ScrapeDate'] = scrape_dict['scrape_date']
    parse_frame['Page'] = scrape_dict['page']

    return parse_frame

july13_scrape_files = [f for f in os.listdir(ROOT_SAVE_DIR) if ('2018-07-13' in f)]

failed_files = []

for i, scrape_batch in enumerate(batch(july13_scrape_files, 1000)):
    print(f'Parsing batch number {i}')

    parsed_frames = []
    for scrape_file in scrape_batch:
        try:
            file_path = os.path.join(ROOT_SAVE_DIR, scrape_file)
            parse_frame = parse_glassdoor_file(file_path)
            parsed_frames.append(parse_frame)
        except Exception as e:
            print(f'{scrape_file} failed.')
            failed_files.append(scrape_file)

    batch_df = pd.concat(parsed_frames)

    clean_path = os.path.join(PARSED_DATA_DIR, f'Glassdoor_Batch_{i}_{TODAY}.csv')
    batch_df.to_csv(clean_path, index=False, sep='\t')


# Read everything into a single DataFrame, set the column order and convert date columns
parsed_files = [f for f in os.listdir(PARSED_DATA_DIR) if (f.endswith('.csv')) & (TODAY in f)]

def read_file(f):
    return pd.read_csv(os.path.join(PARSED_DATA_DIR, f), sep='\t')

col_order = ['Company', 'Date', 'Pros', 'Cons', 'Helpful', 'Page', 'Url', 'ScrapeDate']
df = (pd.concat(read_file(f) for f in parsed_files)
        .loc[:, col_order]
        .assign(Date=lambda x: pd.to_datetime(x['Date']),
                ScrapeDate=lambda x: pd.to_datetime(x['ScrapeDate'])))

# Detect the language of each review
def detect_language(review):
    try:
        lang = ld.detect(review)
        return lang
    except:
        return 'ca'

df['Language'] = df['Pros'].apply(detect_language)

# Write out the unfiltered and English-only to tab-delimited files.
df.to_csv(os.path.join(PARSED_DATA_DIR, f'Glassdoor_Combined_{TODAY}.csv'), index=False, sep='\t')
eng_df = df.loc[df['Language'] == 'en']
eng_df.to_csv(os.path.join(PARSED_DATA_DIR, f'Glassdoor_English_{TODAY}.csv'), index=False, sep='\t')