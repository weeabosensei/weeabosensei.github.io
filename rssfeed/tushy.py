import requests 
from bs4 import BeautifulSoup as bs
from pprint import pprint 
import datetime 
from rfeed import *
import json
from datetime import datetime

# https://github.com/svpino/rfeed

DOMAIN = "https://tushy.com"

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

    return data

def getFeed():
    feedItems = []

    r = requests.get("https://www.tushy.com/videos")

    html = r.text
    page = bs(html,"html.parser")

    items = page.select("div.Grid__Item-f0cb34-1")

    print(len(items))

    for item in items:
        linkBS = item.find('a')
        link =  DOMAIN + linkBS["href"]
        print(link)
        data = getPageDetails(link)
        # pprint(data)cd 

        feedItem = Item(
            title = data['title'],
            link = link, 
            description = data['description'],
        # author = "Santiago L. Valdarrama",
            guid = Guid(link),
            enclosure=Enclosure(url=data['thumbnail'], length=1, type='image'),
            pubDate = datetime.strptime(data['releaseDate'][:10], "%Y-%m-%d")) #datetime.datetime(2014, 12, 29, 10, 00))

        feedItems.append(feedItem)

    feed = Feed(
        title = "Tushy",
        link = "http://www.example.com/rss",
        description = "Tushy.com feed",
        language = "en-US",
        lastBuildDate = datetime.now(),
        items = feedItems)

    content = feed.rss()

    with open('tushy.xml', 'w') as outfile:
        json.dump(content, outfile)


getFeed()