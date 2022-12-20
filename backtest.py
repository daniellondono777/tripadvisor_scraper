from cgitb import text
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


# # Extract the HTML and create a BeautifulSoup object.
# url = ('https://www.tripadvisor.com/Hotels-g294073-Colombia-Hotels.html')

user_agent = ({'User-Agent':
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
			AppleWebKit/537.36 (KHTML, like Gecko) \
			Chrome/90.0.4430.212 Safari/537.36',
			'Accept-Language': 'en-US, en;q=0.5'})

def get_page_contents(url):
    page = requests.get(url, headers = user_agent)
    return BeautifulSoup(page.text, 'html.parser')

# soup = get_page_contents(url)

# hotels = []
# for name in soup.findAll('div',{'class':'listing_title'}):
#     hotels.append(name.text.strip())

# print(hotels)

pattern = '\/Hotel_Review-\w*-\w*-\w*-\w*-\w*.html$'

def main(url):
    city_page_url = 'https://www.tripadvisor.com{url}'.format(url = url)
    soup = get_page_contents(city_page_url)
    content = soup.find_all('div', {'class':'prw_rup prw_meta_hsx_responsive_listing ui_section listItem'})
    for subcontent in content:
        content_subcontent = subcontent.find_all('a')
        for content_url in content_subcontent:
            if re.match(pattern, str(content_url['href'])):
                
                print(content_url['href'])
                


main('/Hotels-g1178558-Barichara_Santander_Department-Hotels.html')


