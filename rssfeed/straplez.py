import requests 
from bs4 import BeautifulSoup as bs
from pprint import pprint 
import datetime 
from rfeed import *
import json
from datetime import datetime

# https://github.com/svpino/rfeed

SITE = "Straplez"
FILENAME = "straplez.xml"
DOMAIN = "https://straplez.com"

def getPageDetails(url):
    r = requests.get(url)

    html = r.text
    page = bs(html,"html.parser")

    item=page.select_one('script[id="__NEXT_DATA__"]').text
    # pprint(item)
    jsondata=json.loads(item)['props']['pageProps']
    # pprint(jsondata['props']['pageProps'])

    data = {}
    models = ', '.join([x['name'] for x in jsondata['video']['modelsSlugged']])
    data["releaseDate"] = jsondata['releaseDate']
    data["title"] = jsondata['title'] + ' - ' + models
    data["description"] = jsondata['description']
    data["thumbnail"] = jsondata['structuredData']['thumbnailUrl']
    data['link'] = url

    return data

def genFeed():
    feedItems = []

    r = requests.get(DOMAIN + "/updates")

    html = r.text
    page = bs(html,"html.parser")

    pprint(page)
    with open("straplez.html", 'w') as outfile:
        outfile.write(html)
    items = page.select("div.item update-stream-card-wrapper")

    print(len(items))

    for item in items:
        linkBS = item.find('a')
        link =  DOMAIN + linkBS["href"]
        print(link)
        data = getPageDetails(link)
        pprint(data)
        break

        thumbnail = '<img src="{}" alt="" />'.format(data['thumbnail']) if data['thumbnail'] else ""

        description = """<![CDATA[
{} 
{}]>""".format(thumbnail, data['description'])

        feedItem = Item(
            title = data['title'],
            link = link, 
            description = description,
        # author = "Santiago L. Valdarrama",
            guid = Guid(link),
            enclosure=Enclosure(url=data['thumbnail'], length=1, type='image'),
            pubDate = datetime.strptime(data['releaseDate'][:10], "%Y-%m-%d")) #datetime.datetime(2014, 12, 29, 10, 00))

        feedItems.append(feedItem)

        feedItems.append(feedItem)

    # feed = Feed(
    #     title = SITE,
    #     link = "http://www.example.com/rss",
    #     description = SITE,
    #     language = "en-US",
    #     lastBuildDate = datetime.now(),
    #     items = feedItems)

    # content = feed.rss()

    # with open(FILENAME, 'w') as outfile:
    #     outfile.write(content)


genFeed()