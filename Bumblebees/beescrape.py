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
        return response.json()

    def parse_sightings(self, data):
        # TODO pull in sightingstatus_id (1 = not verified, 2 = verified)
        # Make list of dictionary keys to be kept
        keepers = ["bee_id", "common_name", "floral_host", "latitude",
                   "longitude", "dateidentified", "sightingstatus_id"]

        # temporary container for bee ids on a particular page
        tmp_list = []
        # for each observation
        for entry in data["data"]["data"]:
            keeper_attrs = {}
            # for the details in that observation
            for elmnt in entry:
                # if the details are what we want, but the k:v in a list
                if elmnt in keepers:
                    keeper_attrs[elmnt] = entry[elmnt]
            # make a key from bee_id so it will be unique across pages/observations
            data = {entry["bee_id"]:keeper_attrs}
            tmp_list.append(data)
        return tmp_list

    def run(self):
        for page in range(1,17):
            # Retrieve data for the page
            data = self.get_bee_sightings(self.API_url_front + str(page) + self.API_url_back)
            print ('scraped page {}'.format(str(page)))
            # parse the data, returning desired attributes
            keeper_data = self.parse_sightings(data)
            print ("Keeper data for page {}: ".format(str(page)))
            print (keeper_data)
            # extend scraped_pages (rather than append) to eliminate the [] from each page's tmp_list
            self.scraped_pages.extend(keeper_data)

        self.save_data()

    def save_data(self):
        with open('bee_sightings.json', 'w') as json_file:
            json.dump(self.scraped_pages, json_file, indent=2)

if __name__ == '__main__':
    scraper = XercesScraper()
    scraper.run()
