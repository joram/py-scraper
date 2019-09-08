#!/usr/bin/env python3
import time
from base import Item, Scraper


class ListPage(Item):

    def details(self):
        soup = self.get_soup()
        camera_urls = []
        for camera in soup.findAll("div", {"class": "product"}):
            a = camera.find("a")
            camera_urls.append(a.attrs["href"])
        return camera_urls

    def next(self):
        soup = self.get_soup()
        pager = soup.find("div", {"class": "pager"})

        current_page = False
        for li in pager.findAll("li"):
            a = li.find("a")
            if current_page:
                return ListPage(a.attrs["href"])
            current_page = "active" in li.attrs["class"]
        return None


class Camera(Item):

    def details(self):
        soup = self.get_soup()
        try:
            name = soup.find("h1", {"itemprop": "name"}).text
        except:
            name = ""

        try:
            image_url = soup.find("meta", {"itemprop": "image"}).attrs["content"]
        except:
            image_url = ""

        try:
            price = soup.find("span", {"class": "price"}).text
        except:
            price = ""

        try:
            description = soup.find("div", {"class": "info"}).text.replace("\n", " ").replace("  ", " ")
        except:
            description = ""

        return {
            "name": name.strip(),
            "image_url": image_url,
            "price": price.strip(),
            "description": description,
            "url": self.url
        }


list_page_s = Scraper("https://www.camera-traders.com/used/", ListPage)
for list_page in list_page_s.run():
    for url in list_page.details():
        page = Camera(url)
        camera = page.details()
        if "Sony E-mount".lower() in camera["description"].lower():
            print(camera["price"].ljust(20, " "), camera["name"].ljust(50), camera["url"])
            time.sleep(1)
