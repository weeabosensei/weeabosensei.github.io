import requests 
from bs4 import BeautifulSoup as bs
from pprint import pprint 
import json
from feedgen.feed import FeedGenerator
import feedutils

SITE = "Throated"
FILENAME = "throated.xml"
DOMAIN = "https://throated.com"

def getPageDetails(url):
    r = requests.get(url)

    html = r.text
    page = bs(html,"html.parser")

    data = {}
    data['title'] = page.find("meta", property="og:title")['content']
    data['description'] = page.find("meta", property="og:description")['content']
    data['thumbnail'] = page.find("meta", property="og:image")['content']
    # data['thumbnail'] = page.find("p.updatedDate").text.strip()
    data['link'] = url

    return data

def genFeed():
    fg = FeedGenerator() 
    fg.id('http://https://weeabosensei.github.io/rssfeed/'+FILENAME)
    fg.title(SITE)
    fg.author( {'name':'John Doe','email':'john@example.de'} )
    fg.link( href='http://example.com', rel='alternate' )
    fg.description(SITE)
    fg.language('en')

    r = requests.get(DOMAIN + "/en/videos")

    html = r.text
    page = bs(html,"html.parser")

    items = page.select("div.sceneContainer")

    print(SITE, len(items))

    for item in items:
        # pprint(item)
        linkBS = item.select_one('a.imgLink')
        # print(linkBS)
        link =  DOMAIN + linkBS["href"]
        # print(link)

        # data
        data = getPageDetails(link)
        data['dateReleased'] = item.select_one('p.sceneDate').text

        feedutils.addEntry(fg, data, "%m-%d-%Y")

    fg.rss_file(FILENAME)

# genFeed()