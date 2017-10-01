from bs4 import BeautifulSoup
import json
import requests


class SoupScraper:
    def __init__(self, url):
        self.url = url
        self.soup = []

    def scrape(self, num_pages):
        '''Returns beautiful soup object after scraping given URL location across x pages'''
        for page in range(1, num_pages + 1):
            if page == 1:
                resp = requests.get(self.url)
            else:
                resp = requests.get(self.url + '&start=' + str(page * 10))
            print(f"Scraping page {page}...")
            soup_page = BeautifulSoup(resp.text, 'html.parser')
            self.soup.append(soup_page)


class SoupParser:
    def __init__(self, SoupScraper):
        self.soup = SoupScraper.soup

    def get_contents_of_tag_type(self, tag, start=0, stop=None):
        '''Returns a list of all contents in a given tag'''
        tags = [[tag.contents[start:stop] for tag in page.select(tag)] for page in self.soup]
        flat_list = [item for sublist in tags for item in sublist]
        return flat_list

    def to_json(self, list_data):
        '''Pickles scraped data for later use'''
        with open('jobs.json', 'w') as js_file:
            json.dump(list_data, js_file)


if __name__ == '__main__':
    scraper = SoupScraper('https://www.indeed.com/jobs?q=python&l=Portland%2C+OR')
    scraper.scrape(34)
    parser = SoupParser(scraper)
    data = parser.get_contents_of_tag_type('span.experienceList')
    print(data)
    parser.to_json(data)
