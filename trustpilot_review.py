import requests, re, csv
import pandas as pd
from bs4 import BeautifulSoup

class TrustpilotReview:
    def __init__(
        self,
        country: str,
        name: str,
        rating: str,
        posted_date: str,
        header: str,
        content: str
    ):
        self.country = country
        self.name = name        
        self.rating = rating
        self.posted_date = posted_date
        self.header = header
        self.content = content

    @staticmethod
    def reviews_from_html(html, country):
        reviews = []
        
        for rev in html.find_all('article')        :
            name = rev.find_all("span", {"data-consumer-name-typography": "true"})[0].text
            rating = rev('section')[0]('div', class_=lambda value: value and value.startswith("styles_reviewHeader"))[0].get('data-service-review-rating')        
            posted_date = rev('section')[0]('time')[0].get('datetime')[0:10]
            header = rev('section')[0]('a')[0].text
            if not rev('section')[0]('div', class_=lambda value: value and value.startswith("styles_reviewContent"))[0]('p'):
                content = ""
            else:
                content = rev('section')[0]('div', class_=lambda value: value and value.startswith("styles_reviewContent"))[0]('p')[0].text
            review = TrustpilotReview(country=country, name=name, rating=rating, posted_date=posted_date, header=header, content=content)
            reviews.append(review)
        return reviews

    def __iter__(self):
        return iter([self.country, self.name, self.rating, self.posted_date, self.header, self.content])