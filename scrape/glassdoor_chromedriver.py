'''
glassdoor_chromedriver.py. This module runs a Selenium/ChromeDriver crawler on Glassdoor instead of Scrapy. I get a
bunch of Latin gibberish when I use Scrapy :| :| :|.
'''

import time
import math
import json
import re
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from lxml import html


TODAY = datetime.now().strftime('%Y-%m-%d')
ROOT_SAVE_DIR = Path(r'C:\Users\rmdelgad\Documents\Berkeley MIDS\W266 Natural Language Processing\Final Project\Glassdoor\raw_data')

company_urls = [
    'https://www.glassdoor.com/Reviews/United-Airlines-Reviews-E683.htm',
    'https://www.glassdoor.com/Reviews/Smile-Brands-Reviews-E321628.htm',
    'https://www.glassdoor.com/Reviews/Memorial-Sloan-Kettering-Reviews-E4711.htm',
    'https://www.glassdoor.com/Reviews/Capital-Group-Reviews-E9441.htm',
    'https://www.glassdoor.com/Reviews/Protiviti-Reviews-E30849.htm',
    'https://www.glassdoor.com/Reviews/E-and-J-Gallo-Winery-Reviews-E2778.htm',
    'https://www.glassdoor.com/Reviews/Oshkosh-Corporation-Reviews-E1740.htm',
    'https://www.glassdoor.com/Reviews/Kronos-Incorporated-Reviews-E2196.htm',
    'https://www.glassdoor.com/Reviews/Taylor-Morrison-Reviews-E37887.htm',
    'https://www.glassdoor.com/Reviews/Progressive-Leasing-Reviews-E665607.htm',
    'https://www.glassdoor.com/Reviews/Wegmans-Food-Markets-Reviews-E3042.htm',
    'https://www.glassdoor.com/Reviews/VMware-Reviews-E12830.htm',
    'https://www.glassdoor.com/Reviews/Hyatt-Reviews-E2839.htm',
    'https://www.glassdoor.com/Reviews/Ellie-Mae-Reviews-E260441.htm',
    'https://www.glassdoor.com/Reviews/Kaiser-Permanente-Reviews-E19466.htm',
    'https://www.glassdoor.com/Reviews/Morrison-Healthcare-Reviews-E5949.htm',
    'https://www.glassdoor.com/Reviews/NVIDIA-Reviews-E7633.htm',
    'https://www.glassdoor.com/Reviews/NIKE-Reviews-E1699.htm',
    'https://www.glassdoor.com/Reviews/Slalom-Reviews-E31102.htm',
    'https://www.glassdoor.com/Reviews/Massachusetts-General-Hospital-Reviews-E20189.htm',
    'https://www.glassdoor.com/Reviews/Stryker-Reviews-E1918.htm',
    'https://www.glassdoor.com/Reviews/Darden-Reviews-E4160.htm',
    'https://www.glassdoor.com/Reviews/H-E-B-Reviews-E2824.htm',
    'https://www.glassdoor.com/Reviews/St-Jude-Children-s-Research-Hospital-Reviews-E28315.htm',
    'https://www.glassdoor.com/Reviews/SpaceX-Reviews-E40371.htm',
    'https://www.glassdoor.com/Reviews/Northwestern-Mutual-Reviews-E2919.htm',
    'https://www.glassdoor.com/Reviews/Boston-Consulting-Group-Reviews-E3879.htm',
    'https://www.glassdoor.com/Reviews/QuikTrip-Reviews-E2947.htm',
    'https://www.glassdoor.com/Reviews/lululemon-Reviews-E42589.htm',
    'https://www.glassdoor.com/Reviews/Johnson-and-Johnson-Reviews-E364.htm',
    'https://www.glassdoor.com/Reviews/Eli-Lilly-and-Company-Reviews-E223.htm',
    'https://www.glassdoor.com/Reviews/REI-Reviews-E7319.htm',
    'https://www.glassdoor.com/Reviews/Zillow-Reviews-E40802.htm',
    'https://www.glassdoor.com/Reviews/Power-Home-Remodeling-Reviews-E405781.htm',
    'https://www.glassdoor.com/Reviews/NewYork-Presbyterian-Hospital-Reviews-E121522.htm',
    'https://www.glassdoor.com/Reviews/Bain-and-Company-Reviews-E3752.htm',
    'https://www.glassdoor.com/Reviews/Yahoo-Reviews-E5807.htm',
    'https://www.glassdoor.com/Reviews/J-Crew-Reviews-E2848.htm',
    'https://www.glassdoor.com/Reviews/Trader-Joe-s-Reviews-E5631.htm',
    'https://www.glassdoor.com/Reviews/Keller-Williams-Reviews-E114145.htm',
    'https://www.glassdoor.com/Reviews/Aurora-Health-Care-Reviews-E121528.htm',
    'https://www.glassdoor.com/Reviews/Boston-Scientific-Reviews-E2187.htm',
    'https://www.glassdoor.com/Reviews/Accenture-Reviews-E4138.htm',
    'https://www.glassdoor.com/Reviews/Starbucks-Reviews-E2202.htm',
    'https://www.glassdoor.com/Reviews/Chick-fil-A-Reviews-E5873.htm',
    'https://www.glassdoor.com/Reviews/Procter-and-Gamble-Reviews-E544.htm',
    'https://www.glassdoor.com/Reviews/Roche-Reviews-E3480.htm',
    'https://www.glassdoor.com/Reviews/adidas-Reviews-E10692.htm',
    'https://www.glassdoor.com/Reviews/Fast-Enterprises-Reviews-E241404.htm',
    'https://www.glassdoor.com/Reviews/Facebook-Reviews-E40772.htm',
    'https://www.glassdoor.com/Reviews/Academy-Mortgage-Reviews-E336856.htm',
    'https://www.glassdoor.com/Reviews/Deloitte-Reviews-E2763.htm',
    'https://www.glassdoor.com/Reviews/BAYADA-Home-Health-Care-Reviews-E153924.htm',
    'https://www.glassdoor.com/Reviews/SAP-Reviews-E10471.htm',
    'https://www.glassdoor.com/Reviews/Paylocity-Reviews-E29987.htm',
    'https://www.glassdoor.com/Reviews/CDW-Reviews-E2347.htm',
    'https://www.glassdoor.com/Reviews/Ceridian-Reviews-E179.htm',
    'https://www.glassdoor.com/Reviews/Salesforce-Reviews-E11159.htm',
    'https://www.glassdoor.com/Reviews/Guidewire-Reviews-E122537.htm',
    'https://www.glassdoor.com/Reviews/Kwik-Trip-Reviews-E18377.htm',
    'https://www.glassdoor.com/Reviews/Electronic-Arts-Reviews-E1628.htm',
    'https://www.glassdoor.com/Reviews/Adobe-Reviews-E1090.htm',
    'https://www.glassdoor.com/Reviews/Texas-Health-Resources-Reviews-E7647.htm',
    'https://www.glassdoor.com/Reviews/In-N-Out-Burger-Reviews-E14276.htm',
    'https://www.glassdoor.com/Reviews/Yardi-Systems-Reviews-E31057.htm',
    'https://www.glassdoor.com/Reviews/Arm-Reviews-E7834.htm',
    'https://www.glassdoor.com/Reviews/Apple-Reviews-E1138.htm',
    'https://www.glassdoor.com/Reviews/McKinsey-and-Company-Reviews-E2893.htm',
    'https://www.glassdoor.com/Reviews/The-Church-of-Jesus-Christ-of-Latter-day-Saints-Reviews-E122747.htm',
    'https://www.glassdoor.com/Reviews/Intuit-Reviews-E2293.htm',
    'https://www.glassdoor.com/Reviews/Toyota-North-America-Reviews-E3544.htm',
    'https://www.glassdoor.com/Reviews/Forrester-Reviews-E6443.htm',
    'https://www.glassdoor.com/Reviews/Monsanto-Company-Reviews-E11986.htm',
    'https://www.glassdoor.com/Reviews/Microsoft-Reviews-E1651.htm',
    'https://www.glassdoor.com/Reviews/Ultimate-Software-Reviews-E7900.htm',
    'https://www.glassdoor.com/Reviews/Delta-Air-Lines-Reviews-E197.htm',
    'https://www.glassdoor.com/Reviews/Blizzard-Entertainment-Reviews-E24858.htm',
    'https://www.glassdoor.com/Reviews/SAP-Concur-Reviews-E8763.htm',
    'https://www.glassdoor.com/Reviews/Capital-One-Reviews-E3736.htm',
    'https://www.glassdoor.com/Reviews/Walt-Disney-Company-Reviews-E717.htm',
    'https://www.glassdoor.com/Reviews/Hilton-Reviews-E330.htm',
    'https://www.glassdoor.com/Reviews/T-Mobile-Reviews-E9302.htm',
    'https://www.glassdoor.com/Reviews/Travelers-Reviews-E1904.htm',
    'https://www.glassdoor.com/Reviews/Liberty-National-Reviews-E19017.htm',
    'https://www.glassdoor.com/Reviews/DocuSign-Reviews-E307604.htm',
    'https://www.glassdoor.com/Reviews/NestlÃ©-Purina-Reviews-E14081.htm',
    'https://www.glassdoor.com/Reviews/Cisco-Systems-Reviews-E1425.htm',
    'https://www.glassdoor.com/Reviews/Google-Reviews-E9079.htm',
    'https://www.glassdoor.com/Reviews/Discount-Tire-Reviews-E6632.htm',
    'https://www.glassdoor.com/Reviews/KPMG-Reviews-E2867.htm',
    'https://www.glassdoor.com/Reviews/LinkedIn-Reviews-E34865.htm',
    'https://www.glassdoor.com/Reviews/World-Wide-Technology-Reviews-E9553.htm',
    'https://www.glassdoor.com/Reviews/HubSpot-Reviews-E227605.htm',
    'https://www.glassdoor.com/Reviews/Kimpton-Hotels-and-Restaurants-Reviews-E9955.htm',
    'https://www.glassdoor.com/Reviews/Extra-Space-Reviews-E35227.htm',
    'https://www.glassdoor.com/Reviews/Insperity-Reviews-E3608.htm',
    'https://www.glassdoor.com/Reviews/AvalonBay-Communities-Reviews-E2616.htm',
    'https://www.glassdoor.com/Reviews/Southwest-Airlines-Reviews-E611.htm',
    'https://www.glassdoor.com/Reviews/Shell-Reviews-E5833.htm',
    'https://www.glassdoor.com/Reviews/3M-Reviews-E446.htm'
]
    
# Initialize ChromeDriver
CHROMEDRIVER_EXE = r'C:\Users\rmdelgad\Documents\ChromeDriver\chromedriver.exe'
driver = webdriver.Chrome(CHROMEDRIVER_EXE)

# Visit start url
start_url = 'https://www.glassdoor.com/profile/login_input.htm?userOriginHook=HEADER_SIGNIN_LINK'
driver.get(start_url)

# Log In
USERNAME = 'ryandelgado8@gmail.com'
PASSWORD = '***'

uname_elem = driver.find_element_by_xpath('')
pw_elem = driver.find_element_by_xpath('')
login_button_elem = driver.find_element_by_xpath('')

uname_elem.send_keys(USERNAME)
pw_elem.send_keys(PASSWORD)
login_button_elem.click()


def save_scrape_dict(scrape_dict, filename):
    file_path = str(ROOT_SAVE_DIR / filename)
    with open(file_path, 'w') as f:
        json.dump(scrape_dict, f)

        
def scrape_review_pg(pg_url, company_name, pg_no):
    driver.get(pg_url)
    time.sleep(1)
    
    page = driver.page_source
    scrape_dict = {
        'body': page,
        'url': driver.current_url,
        'company_name': company_name,
        'scrape_date': TODAY,
        'page': pg_no
    }
    save_scrape_dict(scrape_dict, f'{company_name}_1_{TODAY}.json')


def scrape_company(company_url):
    # Visit the first page and scrape it down
    driver.get(company_url)
    page = driver.page_source
    tree = html.fromstring(page)

    # Parse out company name
    company_name = (tree.xpath('//div[@class="header cell info"]/p[@class="h1 strong tightAll"]/text()')[0]
                    .strip()
                    .replace(' ', ''))

    print(f'Scraping page 1 of {company_name}')

    # Determine the number of review pages
    reviewno_pattern = r'Showing ((?:\d+,){0,5}\d+) of (?:\d+,){0,5}\d+ reviews'
    num_reviews = re.search(reviewno_pattern, page)
    if not num_reviews:
        print(page)
        raise ValueError('Missing number of reviews from page')
    num_reviews = int(num_reviews.group(1).replace(',', ''))
    num_pages = int(math.ceil(num_reviews / 10))

    # Save the first page of reviews as page 1
    scrape_dict = {
        'body': page,
        'url': driver.current_url,
        'company_name': company_name,
        'scrape_date': TODAY,
        'page': 1
    }
    save_scrape_dict(scrape_dict, f'{company_name}_1_{TODAY}.json')

    base_url_nohtm = driver.current_url.replace('.htm', '')

    # Iterate over the second review page to the last page
    for pg_no in range(2, num_pages + 1):
        print(f'Scraping page {pg_no} of {company_name}')
        pg_url = f'{base_url_nohtm}_P{pg_no}.htm'
        scrape_review_pg(pg_url, company_name, pg_no)
        
        
for company_url in company_urls:
    scrape_company(company_url)