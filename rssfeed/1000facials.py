import requests 
from bs4 import BeautifulSoup as bs
from pprint import pprint 
import datetime 
from rfeed import *
import json
from datetime import datetime

# https://github.com/svpino/rfeed

SITE = "1000 Facials"
FILENAME = "1000facials.xml"
DOMAIN = "https://1000facials.com"

def getPageDetails(url):
    r = requests.get(url)

    html = r.text
    page = bs(html,"html.parser")

    

    # item=page.select_one('script[id="__NEXT_DATA__"]').text

#     item=page.select_one('script[id="__NEXT_DATA__"]').text
#     # pprint(item)
#     jsondata=json.loads(item)['props']['pageProps']
#     # pprint(jsondata['props']['pageProps'])

    data = {}
    
    data['title'] = page.select_one('h1.title').text

    # meta = 
    data['description'] = page.find("meta", attrs={'name': 'description'})['content']
    data['thumbnail'] = None #page.find("meta", property="og:image")['content']
    # data['releaseDate'] = page.find("meta", property="og:image")
#     models = ', '.join([x['name'] for x in jsondata['video']['modelsSlugged']])
#     data["releaseDate"] = jsondata['releaseDate']
#     data["title"] = jsondata['title'] + ' - ' + models
#     data["description"] = jsondata['description']
#     data["thumbnail"] = jsondata['structuredData']['thumbnailUrl']

    return data

def genFeed():
    feedItems = []

    r = requests.get(DOMAIN + "/en/scenes")

    html = r.text
    page = bs(html,"html.parser")

    items = page.select("div.tlcItem")

    print(len(items))

    for item in items:
        # pprint(item)
        linkBS = item.find('a')
        # print(linkBS)
        link =  DOMAIN + linkBS["href"]
        # print(link)

        # data
        data = getPageDetails(link)

        # pprint(data)

        dateReleased = item.select_one('span.tlcSpecsDate').select_one('span.tlcDetailsValue').text

        thumbBS = linkBS.find('img')
        data['thumbnail'] = thumbBS['src'] if thumbBS else None
        
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
            pubDate = datetime.strptime(dateReleased, "%Y-%m-%d"))

        feedItems.append(feedItem)

    feed = Feed(
        title = SITE,
        link = "http://www.example.com/rss",
        description = SITE,
        language = "en-US",
        lastBuildDate = datetime.now(),
        items = feedItems)

    content = feed.rss()

    with open(FILENAME, 'w') as outfile:
        outfile.write(content)


# genFeed()