import json
from flask import Flask, render_template, request
from scraper import Scraper

app = Flask("Trip Advisor Scraper")

@app.route('/scrap')
def scraper_endpoint():
    '''
    (200) Returns in a csv the requested information
    '''
    ciudad = request.get_json()['ciudad']
    scraper = Scraper(ciudad)
    return scraper.str_detailed_info_csv()

if __name__ == '__main__':
    app.run()