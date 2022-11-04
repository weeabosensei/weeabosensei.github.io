import requests 
from bs4 import BeautifulSoup as bs
from pprint import pprint 
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
import feedutils

SITE = "Blacked"
FILENAME = "blacked.xml"
DOMAIN = "https://blacked.com"

def genFeed():
    fg = FeedGenerator() 
    fg.id('http://https://weeabosensei.github.io/rssfeed/'+FILENAME)
    fg.title(SITE)
    fg.author( {'name':'John Doe','email':'john@example.de'} )
    fg.link( href='http://example.com', rel='alternate' )
    fg.description(SITE)
    # fg.logo('http://ex.com/logo.jpg')
    # fg.subtitle('This is a cool feed!')
    # fg.link( href='http://larskiesow.de/test.atom', rel='self' )

    r = requests.get(DOMAIN + "/videos")

    html = r.text
    page = bs(html,"html.parser")

    items = page.select("div.Grid__Item-f0cb34-1")

    print(SITE, len(items))

    for item in items:
        linkBS = item.find('a')
        link =  DOMAIN + linkBS["href"]
        print(link)
        data = feedutils.getPageDetailsTushy(link)
        # pprint(data)cd 

        feedutils.addEntry(fg, data)

    fg.rss_file(FILENAME)

# genFeed()