import requests 
from bs4 import BeautifulSoup as bs
from pprint import pprint 
from feedgen.feed import FeedGenerator
import feedutils

SITE = "Only Teen Blowjobs"
FILENAME = "onlyteenblowjobs.xml"
DOMAIN = "https://onlyteenblowjobs.com"

def getPageDetails(url):
    r = requests.get(url)

    html = r.text
    page = bs(html,"html.parser")

    data = {}
    data['title'] = page.find("meta", property="og:title")['content']
    data['description'] = page.find("meta", property="og:description")['content']
    data['thumbnail'] = page.find("meta", property="og:image")['content']
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
        # print(linkBS)
        link =  DOMAIN + linkBS["href"]
        # print(link)

        # data
        data = getPageDetails(link)

        # pprint(data)

        data['dateReleased'] = item.select_one('span.tlcSpecsDate').select_one('span.tlcDetailsValue').text
        
        feedutils.addEntry(fg, data, "%m-%d-%Y")

    fg.rss_file(FILENAME)


# genFeed() 