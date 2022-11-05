import requests 
from bs4 import BeautifulSoup as bs
from pprint import pprint 
from feedgen.feed import FeedGenerator

import feedutils

SITE = "21 Erotic Anal"
FILENAME = "21eroticanal.xml"
DOMAIN = "https://21eroticanal.net/"

def getPageDetails(item):
    data = {}

    linkBS = item.find('a')
   
    
    data['title'] = linkBS['title']

    data['description'] = item.select_one('#starrings').text.strip()
    data['thumbnail'] =  item.find("img")['src']
    data['link'] = linkBS["href"]

    dateText = item.select_one('ul.post-meta > li > span').text.strip() #[0].text
    # print(dateText)
    data['dateReleased'] = feedutils.fromDateWords(dateText)
    
    # pprint(data)

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

    r = requests.get(DOMAIN)

    html = r.text
    page = bs(html,"html.parser")

    items = page.select("div.category-episodes")

    print(SITE, len(items))

    for item in items:
        data = getPageDetails(item)

        feedutils.addEntry(fg, data)

    fg.rss_file(FILENAME)


# genFeed()