
import requests 
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime, timedelta, timezone

def addEntry(fg, data, dateFormat="%Y-%m-%d"):
    imageUrl = data['thumbnail'].split('?')[0] if data['thumbnail'] else None
    thumbnail = '<img src="{}" alt="" />'.format(imageUrl) if imageUrl else None

    description = "{} {}".format(thumbnail, data['description'])

    fe = fg.add_entry(order='append')
    fe.id(data['link'])
    fe.title(data['title'])
    fe.link(href=data['link'])
    fe.description(data['description'])
    fe.content(description, type='CDATA')
    fe.pubDate(datetime.strptime(data['dateReleased'], dateFormat).replace(tzinfo=timezone.utc))

    if imageUrl:
        fe.enclosure(imageUrl, 0, 'image/jpeg')


## helpers
def fromDateWords(dateString):
    newDate = None

    if dateString.lower() == 'today':
        newDate = datetime.today()
    if dateString.lower() == 'yesterday':
        newDate = datetime.today() - timedelta(days=1)
    if dateString.lower() == '2 days ago':
        newDate = datetime.today() - timedelta(days=2)
    else:
        newDateString = dateString.replace('st,', '').replace('nd,','').replace('rd,','').replace('th,', '')
        newDate = datetime.strptime(newDateString, "%B %d %Y")

    return newDate.strftime("%Y-%m-%d")

# per site 
# tushy

def getPageDetailsTushy(url):
    r = requests.get(url)

    html = r.text
    page = bs(html,"html.parser")

    item=page.select_one('script[id="__NEXT_DATA__"]').text

    jsondata=json.loads(item)['props']['pageProps']


    data = {}
    models = ', '.join([x['name'] for x in jsondata['video']['modelsSlugged']])
    data["dateReleased"] = jsondata['releaseDate'][:10]
    data["title"] = jsondata['title'] + ' - ' + models
    data["description"] = jsondata['description']
    data["thumbnail"] = jsondata['structuredData']['thumbnailUrl']
    data['link'] = url

    return data
