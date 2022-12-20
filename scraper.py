from urllib.request import urlopen, Request
from wsgiref import headers
import requests
import ssl
import requests
from bs4 import BeautifulSoup
import json
import re
import datetime

ssl._create_default_https_context = ssl._create_unverified_context

class Scraper:
    def __init__(self, city: str) -> None:
        '''
        Constructor method
        '''
        self.city = city
        self.headers = (
                        {   
                        'User-Agent':
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/90.0.4430.212 Safari/537.36',
                        'Accept-Language': 'en-US, en;q=0.5'
                        })

    def get_content(self, url, headers) -> BeautifulSoup:
        '''
        Gets the content (DOM) of a given url
        '''
        page = requests.get(url, headers = headers)
        return BeautifulSoup(page.text, 'html.parser')

    def get_url_hotels_by_city(self) -> str:
        '''
        Returns the URL of TripAdvisor's hotels page for the specified city (destiny)
        '''

        page1_url = 'https://www.tripadvisor.com/Hotels-g294073-Colombia-Hotels.html'
        pages_left_url = 'https://www.tripadvisor.com/Hotels-g294073-oa{part}-Colombia-Hotels.html#LEAF_GEO_LIST'#.format(part=n) n = {20,40,60 ... lim}


        # 1st page includes some cities
        soup_page_1 = self.get_content(url = page1_url, headers= self.headers)
        cities = soup_page_1.find_all('div', {'class':'leaf_geo_list_wrapper entry_point_update'})[0]
        
        # Contains the hrefs of all possible destinies in TripAdvisor
        cities_refs = []

        pattern = '\/\w*-\w*-\w*-\w*.html$'
        for i in cities.find_all('a'):
            if re.match(pattern, str(i['href'])):
                cities_refs.append(str(i['href']))

        # The rest of the pages include the rest of possible destinations in TripAdvisor
        start = 20
        try:
            while True:
                soup_page_n = self.get_content(url = pages_left_url.format(part=str(start)), headers= self.headers)
                cities = soup_page_n.find_all('div', {'class':'ppr_rup ppr_priv_broad_geo_tiles'})[0]
                for i in cities.find_all('a'):
                    if re.match(pattern, str(i['href'])):
                        cities_refs.append(str(i['href']))
                start += 20
        except:
            pass

        r = re.compile(".*{}".format(self.city))
        return list(filter(r.match, cities_refs))[0] # Returns first ocurrence


    def get_city_hotels_urls(self) -> list:
        '''
        Gets all the hotel urls from a given city
        '''
        urls = []
        city_page_url = 'https://www.tripadvisor.com{url}'.format(url = self.get_url_hotels_by_city())
        soup = self.get_content(city_page_url, self.headers)
        content = soup.find_all('div', {'class':'prw_rup prw_meta_hsx_responsive_listing ui_section listItem'})
        pattern = '\/Hotel_Review-\w*-\w*-\w*-\w*-\w*.html$'
        for subcontent in content:
            content_subcontent = subcontent.find_all('a')
            for content_url in content_subcontent:
                if re.match(pattern, str(content_url['href'])):
                    urls.append(content_url['href'])
        nd_urls = [] # non-duplicated urls
        [nd_urls.append(item) for item in urls if item not in nd_urls]
        return nd_urls
    
    def get_hotel_info(self, url) -> list:
        '''
        Returns a hotel information:
        - Hotel id and link to the hotel page on TripAdvisor *  
        - Name, phone number, address, website, and other contact information.
        - Ratings and quality rankings. *
        - Indicative price. *
        - Timestamp of when the data was scraped. *

        '''
        hotel_url = 'https://www.tripadvisor.com{url}'.format(url)



i1 = Scraper('Bucaramanga')

print(i1.get_city_hotels_urls())
