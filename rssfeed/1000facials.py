import requests 
from bs4 import BeautifulSoup as bs
from pprint import pprint 
import datetime 
from feedgen.feed import FeedGenerator
import json
from datetime import datetime, timezone

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
    fg = FeedGenerator() 
    fg.id('http://lernfunk.de/media/654321')
    fg.title(SITE)
    fg.author( {'name':'John Doe','email':'john@example.de'} )
    fg.link( href='http://example.com', rel='alternate' )
    fg.description(SITE)
    # fg.logo('http://ex.com/logo.jpg')
    # fg.subtitle('This is a cool feed!')
    # fg.link( href='http://larskiesow.de/test.atom', rel='self' )
    fg.language('en')
    # feed = Feed(
    #     title = SITE,
    #     link = "http://www.example.com/rss",
    #     description = SITE,
    #     language = "en-US",
    #     lastBuildDate = datetime.now(),
    #     items = feedItems)

    feedItems = []

    r = requests.get(DOMAIN + "/en/scenes")

    html = r.text
    page = bs(html,"html.parser")

    items = page.select("div.tlcItem")

    print(len(items))

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

        dateReleased = item.select_one('span.tlcSpecsDate').select_one('span.tlcDetailsValue').text

        thumbBS = linkBS.find('img')
        data['thumbnail'] = thumbBS['data-original'] if thumbBS else None
        
        thumbnail = '<img src="{}" alt="" />'.format(data['thumbnail']) if data['thumbnail'] else ""

        description = "{} {}".format(thumbnail, data['description'])

        fe = fg.add_entry(order='append')
        fe.id(link)
        fe.title(data['title'])
        fe.link(href=link)
        fe.content(description, type='CDATA')
        fe.pubDate(datetime.strptime(dateReleased, "%Y-%m-%d").replace(tzinfo=timezone.utc))
        fe.enclosure(data['thumbnail'], 0, 'image')

    fg.rss_file(FILENAME)


genFeed()