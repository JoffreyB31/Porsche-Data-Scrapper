import json
import pprint
import urllib.request

from bs4 import BeautifulSoup

PORSCHE_DOMAIN = "https://www.porsche.com"
PORSCHE_CLASSIC_URL = PORSCHE_DOMAIN + "/france/accessoriesandservice/classic/"


def get_soup(url):
    print(f"Requesting {url}")
    html = urllib.request.urlopen(url)
    content = html.read().decode('utf-8', 'ignore')
    return BeautifulSoup(content, "html.parser")


def scrape_model(soup):
    name = soup.select("div.b-title-headline-text h1 span")[0].text
    description = [item.text for item in soup.select("div.b-standard-module div.b-standard-module-wrapper p")]
    img = soup.select("div.b-standard-intro-wrapper img")[0].attrs["data-image-src"]

    return {
        "name": name,
        "description": description,
        "img": img
    }


def get_model_soup(url):
    return scrape_model(get_soup(url))


def scrape_models(url):
    models = []
    skipped_items = ["Catalogue des pièces d'origine", "ORIGINALE", "Documentation historique"]

    soup = get_soup(url)
    items = soup.select("div.b-teaser-wrapper a.b-teaser-link")

    # Redirect either to the generation view or the model view (with the data)
    url_to_scrape = []
    for item in items:
        name = item.find("div", {"class": "b-teaser-caption"}).contents[0].text
        url = item.attrs['href']

        if any(name in s for s in skipped_items):
            continue
        else:
            url_to_scrape.append(PORSCHE_DOMAIN + url)

    if len(url_to_scrape) > 0:
        for url in url_to_scrape:
            models.append(get_model_soup(url))
    else:
        models.append(scrape_model(soup))

    return models


def scrape_generations():
    soup = get_soup(PORSCHE_CLASSIC_URL)
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
with open('data.json', 'w') as f:
    json.dump(generations, f, ensure_ascii=False)
