import requests 
from bs4 import BeautifulSoup as bs
from pprint import pprint 
from feedgen.feed import FeedGenerator

import feedutils

SITE = "1000 Facials"
FILENAME = "1000facials.xml"
DOMAIN = "https://1000facials.com"

def getPageDetails(url):
    r = requests.get(url)

    html = r.text
    page = bs(html,"html.parser")

    data = {}
    
    data['title'] = page.select_one('h1.title').text

    data['description'] = page.select_one('h1.title').text #page.find("meta", attrs={'name': 'description'})['content']
    data['thumbnail'] = None #page.find("meta", property="og:image")['content']
    data['link'] = url

    return data

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
    fg.language('en')

    r = requests.get(DOMAIN + "/en/scenes")

    html = r.text
    page = bs(html,"html.parser")

    items = page.select("div.tlcItem")

    print(SITE, len(items))

    for item in items:
        # pprint(item)
        linkBS = item.find('a')
        # pprint(linkBS)
        # break
        link =  DOMAIN + linkBS["href"]
        # print(link)

        # data
        data = getPageDetails(link)

        # pprint(data)

        data['dateReleased'] = item.select_one('span.tlcSpecsDate').select_one('span.tlcDetailsValue').text

        thumbBS = linkBS.find('img')
        data['thumbnail'] = thumbBS['data-original'] if thumbBS else None

        feedutils.addEntry(fg, data)

    fg.rss_file(FILENAME)


# genFeed()