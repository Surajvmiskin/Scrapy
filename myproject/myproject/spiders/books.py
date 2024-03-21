from typing import Iterable
import scrapy
from pathlib import Path
from pymongo import MongoClient
import datetime


client = MongoClient(
    "mongodb+srv://Suraj:Suraj123@cluster0.uuxn554.mongodb.net/")

db = client.scrapy


def InsertDB(page, tittle, rating, image, price, instock):
    collection = db[page]
    doc = {
        "title": tittle,
        "rating": rating,
        "image": image,
        "price": price,
        "instock": instock,
        "date": datetime.datetime.utcnow()
    }
    inserted = collection.insert_one(doc)
    return inserted.inserted_id


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]

    def start_requests(self):
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        bookdetail = {}

        # Save the content as files
        # Path(filename) .write_bytes(response.body)

        # self. log(f"Saved file {filename}")
        # a = response.css(".product_pod")
        # b = a.css("a")
        # print(b)

        self. log(f"Saved file {filename}")
        cards = response.css(".product_pod")
        for card in cards:
            tittle = card.css("h3>a::text").get()
            # print(tittle)

            rating = card.css(".star-rating").attrib["class"].split(' ')[1]
            # print(rating)

            image = card.css(".image_container img")
            image = image.attrib["src"].replace(
                "../../../../media", "https://books.toscrape.com/media")

            price = card.css(".price_color::text").get().split('£')[1]
            # print(price)

            availability = card.css(".availability")

            if len(availability.css(".icon-ok")) > 0:
                instock = True
            else:
                instock = False

            print(instock)
            InsertDB(page, tittle, rating, image, price, instock)
