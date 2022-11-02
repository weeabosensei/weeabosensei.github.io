import requests 
from bs4 import BeautifulSoup as bs
from pprint import pprint 
import datetime 
from feedgen.feed import FeedGenerator
import json
from datetime import datetime, timezone

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

        dateReleased = item.select_one('span.tlcSpecsDate').select_one('span.tlcDetailsValue').text
        
        thumbnail = '<img src="{}" alt="" />'.format(data['thumbnail']) if data['thumbnail'] else ""

        description = "{} {}".format(thumbnail, data['description'])

        fe = fg.add_entry(order='append')
        fe.id(link)
        fe.title(data['title'])
        fe.link(href=link)
        fe.description(data['description'])
        fe.content(description, type='CDATA')
        fe.pubDate(datetime.strptime(dateReleased, "%m-%d-%Y").replace(tzinfo=timezone.utc))
        fe.enclosure(data['thumbnail'], 0, 'image/jpeg')

    fg.rss_file(FILENAME)


# genFeed() 