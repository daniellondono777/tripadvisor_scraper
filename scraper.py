from urllib.request import urlopen, Request
from wsgiref import headers
import requests
import ssl
import requests
from bs4 import BeautifulSoup
import json
import re
import datetime
import base64
import pandas as pd

ssl._create_default_https_context = ssl._create_unverified_context

class Scraper:
    '''
    Object to scrape TripAdvisor's website and obtain relevant information of hotels in Colombia. 
    '''
    def __init__(self, city: str) -> None:
        '''
        Constructor method
        '''
        self.city = city[0].upper() + city[1::].lower()
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
    
    def mean(self, arr):
            '''
            Helper function to calculate average
            '''
            return sum(arr)/len(arr)
    
    def get_hotel_info(self, url) -> dict:
        '''
        Returns a hotel information:
        - Hotel id and link to the hotel page on TripAdvisor *  
        - Name, phone number, address, website, and other contact information. *
        - Ratings and quality rankings. *
        - Indicative price. *
        - Timestamp of when the data was scraped. *

        '''
        info = dict()
        hotel_url = 'https://www.tripadvisor.com{url}'.format(url=url)
        content = self.get_content(hotel_url, self.headers)
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

        # Name
        name = ''
        try:
            name = content.find_all('h1', {'class':'QdLfr b d Pn'})[0].text
        except:
            pass

        id = url.split('-')[2].split('d')[1]
        address = content.find_all('span', {'class':'fHvkI PTrfg'})[0].text

        # Hotel's Telephone
        telephone = ''
        try:
            telephone = content.find_all('span', {'class':'zNXea NXOxh NjUDn'})[0].text
        except:
            pass

        # Hotel's Adress
        hotel_website = ''
        try:
            hotel_main_url = str(content.find_all('div', {'class':'eeVey S4 H3 f u LGJIs'})[0].find_all('a')[0]['data-encoded-url'])
            if hotel_main_url:
                hotel_website = "https://www.tripadvisor.com" + "/Commerce?p" +str(base64.b64decode(hotel_main_url)).split('/Commerce?p')[1]
        except:
            pass
        
        # Price
        price = 'undisclosed'
        prices = []
        try:
            price = content.find_all('div', {'class':'premium_offers_area offers'})[0] # Price of 1 night for an adult.
            for p in price.find_all('div'):
                try:
                    prices.append(int(p['data-pernight']))
                except:
                    pass
        except:
            pass

        average_price = 0
        if len(prices) > 0:
            average_price = self.mean(prices)
        
        rating = content.find_all('span', {'class':'uwJeR P'})[0].text
        quality_rankings = content.find_all('div', {'class':'WdWxQ'})
        qr_rankings = []
        for qr in quality_rankings:
            q_ranking = []
            for c in qr.find_all('span'):
                q_ranking.append(c.text)
            qr_rankings.append(q_ranking)
        rankings = dict()
        for i in qr_rankings:
            rankings[str(i[0])] = i[1]
        
        info['hotel_name'] = name
        info['hotel_id'] = id
        info['url_trip_advisor'] = hotel_url
        info['hotel_website'] = hotel_website
        info['address'] = address
        info['telephone'] = telephone
        info['average_price'] = average_price
        info['overall_rating'] = rating
        info['quality_rankings'] = rankings
        info['timestamp'] = timestamp

        return info

    
    def get_all_hotel_info_by_city(self) -> pd.DataFrame:
        '''
        Returns in a DataFrame detailed information about Hotels in the specified city. 
        '''
        hotels_by_city = []
        hotels_urls = self.get_city_hotels_urls()
        for el in hotels_urls:
            hotels_by_city.append(self.get_hotel_info(el))
        df = pd.DataFrame.from_dict(hotels_by_city)
        return df
    
    def detailed_info_csv(self) -> None:
        '''
        Exports the Dataframe with detailed information into a .csv file
        '''
        df = self.get_all_hotel_info_by_city()
        df.to_csv('detailed_info_hotels_{c}.csv'.format(c = self.city.lower()))
    
    def str_detailed_info_csv(self) -> str:
        '''
        Returns detailed information in a string with a csv format
        '''
        df = self.get_all_hotel_info_by_city()
        csv_df = df.to_csv()
        return csv_df
