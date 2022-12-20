from cgitb import text
import telnetlib
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np
import datetime
import base64


# # Extract the HTML and create a BeautifulSoup object.
# url = ('https://www.tripadvisor.com/Hotels-g294073-Colombia-Hotels.html')

user_agent = ({'User-Agent':
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
			AppleWebKit/537.36 (KHTML, like Gecko) \
			Chrome/90.0.4430.212 Safari/537.36',
			'Accept-Language': 'en-US, en;q=0.5'})

def get_content(url):
    page = requests.get(url, headers = user_agent)
    return BeautifulSoup(page.text, 'html.parser')

# soup = get_page_contents(url)

# hotels = []
# for name in soup.findAll('div',{'class':'listing_title'}):
#     hotels.append(name.text.strip())

# print(hotels)

# pattern = '\/Hotel_Review-\w*-\w*-\w*-\w*-\w*.html$'

# def main(url):
#     city_page_url = 'https://www.tripadvisor.com{url}'.format(url = url)
#     soup = get_page_contents(city_page_url)
#     content = soup.find_all('div', {'class':'prw_rup prw_meta_hsx_responsive_listing ui_section listItem'})
#     for subcontent in content:
#         content_subcontent = subcontent.find_all('a')
#         for content_url in content_subcontent:
#             if re.match(pattern, str(content_url['href'])):
                
#                 print(content_url['href'])
                


# main('/Hotels-g1178558-Barichara_Santander_Department-Hotels.html')

urls = ['/Hotel_Review-g297474-d940073-Reviews-Hotel_Dann_Carlton_de_Bucaramanga-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d10399087-Reviews-Hampton_by_Hilton_Bucaramanga-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d4860255-Reviews-Holiday_Inn_Bucaramanga_Cacique_an_IHG_Hotel-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d2430739-Reviews-Hotel_Buena_Vista-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d6163888-Reviews-Hotel_Bari_Bucaramanga-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d2666899-Reviews-Cabecera_Country_Hotel-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d4688819-Reviews-Hotel_Palonegro-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d302676-Reviews-Hotel_Chicamocha-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d6899820-Reviews-Hotel_Colonial_Plaza-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d1020445-Reviews-Hotel_Internacional_La_Triada_by_DOT_Urban-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d2355952-Reviews-Hotel_Plazuela_Real-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d5223205-Reviews-Hotel_Buena_Vista_Express-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d1726723-Reviews-Hotel_D_Leon-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d3422273-Reviews-Hotel_Andino-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d7986310-Reviews-Hotel_Bucarica_Plaza-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d1631157-Reviews-Hotel_San_Juan_Internacional-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d15109792-Reviews-BLH_Business_Loft_Hotel-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d1108690-Reviews-Hotel_Ciudad_Bonita-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d3421110-Reviews-Hotel_El_Leon_Dorado-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d7282301-Reviews-BGA_Hotel-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d2666346-Reviews-Hotel_La_Serrania-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d2231870-Reviews-Hotel_San_Jose_Plaza-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d1523295-Reviews-Hotel_Ruitoque_Bucaramanga-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d7651429-Reviews-Hotel_Bucaramanga_Plaza-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d4202771-Reviews-Hotel_Palmera_Real-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d7826973-Reviews-Hotel_San_Rey-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d17518145-Reviews-Ayenda_1508_Hotel_Rubi-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d8655396-Reviews-Hotel_Tachiras-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d12115445-Reviews-Hotel_Isla_Mayor-Bucaramanga_Santander_Department.html', '/Hotel_Review-g297474-d2031932-Reviews-Hotel_Balmoral-Bucaramanga_Santander_Department.html']


def mean(arr):
    '''
    Helper function to calculate average
    '''
    return sum(arr)/len(arr)

def get_hotel_info(url):
    '''
    Returns a Hotel's info given its URL
    '''
    info = dict()
    hotel_url = 'https://www.tripadvisor.com{url}'.format(url=url)
    content = get_content(hotel_url)
    timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    name = content.find_all('h1', {'class':'QdLfr b d Pn'})[0].text
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
        average_price = mean(prices)
    
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
    # info[''hotel_id] = id
    info['url_trip_advisor'] = hotel_url
    info['hotel_website'] = hotel_website
    info['address'] = address
    info['telephone'] = telephone
    info['average_price'] = average_price
    info['overall_rating'] = rating
    info['quality_rankings'] = rankings
    info['timestamp'] = timestamp

    return info
    


for i in urls:
    print(get_hotel_info(i))
    print('********')