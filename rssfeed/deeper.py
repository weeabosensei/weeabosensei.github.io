import requests 
from bs4 import BeautifulSoup as bs
from pprint import pprint 
import datetime 
from feedgen.feed import FeedGenerator
import json
from datetime import datetime, timezone

# https://github.com/svpino/rfeed

SITE = "Deeper"
FILENAME = "deeper.xml"
DOMAIN = "https://deeper.com"


def getPageDetails(url):
    r = requests.get(url)

    html = r.text
    page = bs(html,"html.parser")

    item=page.select_one('script[id="__NEXT_DATA__"]').text

    jsondata=json.loads(item)['props']['pageProps']


    data = {}
    models = ', '.join([x['name'] for x in jsondata['video']['modelsSlugged']])
    data["releaseDate"] = jsondata['releaseDate']
    data["title"] = jsondata['title'] + ' - ' + models
    data["description"] = jsondata['description']
    data["thumbnail"] = jsondata['structuredData']['thumbnailUrl']

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

    r = requests.get(DOMAIN + "/videos")

    html = r.text
    page = bs(html,"html.parser")

    items = page.select("div.Grid__Item-f0cb34-1")

    print(SITE, len(items))

    for item in items:
        linkBS = item.find('a')
        link =  DOMAIN + linkBS["href"]
        print(link)
        data = getPageDetails(link)
        # pprint(data)cd 

        thumbnail = '<img src="{}" alt="" />'.format(data['thumbnail']) if data['thumbnail'] else ""

        description = "{} {}".format(thumbnail, data['description'])

        fe = fg.add_entry(order='append')
        fe.id(link)
        fe.title(data['title'])
        fe.link(href=link)
        fe.description(data['description'])
        fe.content(description, type='CDATA')
        fe.pubDate(datetime.strptime(data['releaseDate'][:10], "%Y-%m-%d").replace(tzinfo=timezone.utc))
        fe.enclosure(data['thumbnail'], 0, 'image/jpeg')

    fg.rss_file(FILENAME)

# genFeed()