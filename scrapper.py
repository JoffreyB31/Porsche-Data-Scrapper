import pprint
import urllib.request

from bs4 import BeautifulSoup

PORSCHE_DOMAIN = "https://www.porsche.com"
PORSCHE_CLASSIC_URL = PORSCHE_DOMAIN + "/france/accessoriesandservice/classic/"


def scrape_models(url):
    models = []

    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    items = soup.select("div.b-teaser-wrapper a.b-teaser-link")

    for item in items:
        model = {
            "name": item.find("div", {"class": "b-teaser-caption"}).contents[0].text,
            "url": PORSCHE_DOMAIN + item.attrs["href"],
            "img": item.find("img").attrs["data-image-src"]
        }
        models.append(model)

    return models


def scrape_generations():
    page = urllib.request.urlopen(PORSCHE_CLASSIC_URL)
    soup = BeautifulSoup(page, 'html.parser')
    timeline_wrapper = soup.find("div", {"class": "m-30-timeline"})
    timeline_items = timeline_wrapper.find_all("div", {"class": "m-30-timeline-item"})

    for timeline_item in timeline_items:
        item_content = timeline_item.find("div", {"class": "m-30-timeline-item-content"})
        date_range = item_content.contents[1].text
        generation = {
            "name": item_content.contents[0].text,
            "start": date_range.split("-")[0],
            "end": date_range.split("-")[1],
            "img": timeline_item.find("img").attrs['src'],
        }

        model_url = PORSCHE_DOMAIN + timeline_item.find("a").attrs['href']
        generation["models"] = scrape_models(model_url)

        generations.append(generation)


generations = []
scrape_generations()
pprint.pprint(generations)
