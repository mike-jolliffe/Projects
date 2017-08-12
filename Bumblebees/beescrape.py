"""Leaned very heavily on the following tutorial for scraping websites that
   utilize AJAX:
   https://www.codementor.io/codementorteam/how-to-scrape-an-ajax-website-using-python-qw8fuitvi"""

# Import dependencies
import json
from lxml.etree import fromstring
import requests

# Create a Scraper object
class XercesScraper:
    # split up url so I can insert a page number later
    API_url_front = 'https://www.bumblebeewatch.org/api/beemetas/list?&limit=20&page='
    API_url_back = '&province_id=50&county_id=320'
    scraped_pages = []

    def get_bee_sightings(self, page):
        """Send a request to the Xerces server"""
        # Making the get request
        response = requests.get(page)

        # We want the first element of response, under key 'data'
        return response.json()['data']

    def parse_sightings(self, data):
        # TODO clean up response JSON, only keeping bee_id, common_name, floral_host,
        #      latitude, longitude, and dateidentified
        pass

    def run(self):
        for page in range(1,17):
            # Retrieve data for page
            data = self.get_bee_sightings(self.API_url_front + str(page) + self.API_url_back)
            print ('scraped page {}'.format(str(page)))
            # TODO identify the exact elements I want to grab. Full dump for now
            self.parse_sightings(data)
            self.scraped_pages.append(data)

        self.save_data()

    def save_data(self):
        with open('bee_sightings.json', 'w') as json_file:
            json.dump(self.scraped_pages, json_file, indent=4)

if __name__ == '__main__':
    scraper = XercesScraper()
    scraper.run()
