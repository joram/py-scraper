import re
import requests
from bs4 import BeautifulSoup


class FailedRequest(Exception):
    pass


class UnImplementedRequest(Exception):
    pass


class Item(object):

    def __init__(self, url, cache=None, debug=False):
        self.url = url
        self.cache = cache
        self.debug = debug
        self.soup = None

    def get_soup(self):
        if self.soup is not None:
            return self.soup
        html = self.get_html()
        self.soup = BeautifulSoup(html, features="lxml")
        return self.soup

    def get_html(self):
        if self.debug:
            print("downloading {}".format(self.url))
        resp = requests.get(self.url)
        if resp.status_code != 200:
            print(FailedRequest(resp.content))
        return str(resp.text)

    def get_metadata(self, soup):
        data = {}

        # opengraph data
        for tag in soup.findAll(property=re.compile(r'^og')):
            key = tag["property"].replace("og:", "")
            val = tag["content"]
            data[key] = val

        # facebook data
        for tag in soup.findAll(property=re.compile(r'^fb')):
            key = tag["property"].replace("fb:", "")
            val = tag["content"]
            data[key] = val

        return data

    def details(self):
        raise UnImplementedRequest()

    def next(self):
        raise UnImplementedRequest()

    def __str__(self):
        return self.url


class Scraper(object):

    def __init__(self, starting_url, item_class=Item, sleep=1):
        self.item_class = item_class
        self.starting_url = starting_url
        self.sleep = sleep

    def run(self, cache=None):
        item = self.item_class(self.starting_url, cache=cache)
        while item is not None:
            yield item
            item = item.next()
