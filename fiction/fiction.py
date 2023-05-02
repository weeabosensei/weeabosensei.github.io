import requests
import json
from bs4 import BeautifulSoup

DOMAIN = 'http://fictionmania.tv'
SEARCH = '/searchdisplay/ratingdisplay.html?startat={}&rate=X'
# https://www.fictionmania.tv/stories/readststory.html?storyID=1611943084142133846
DOWNLOAD = '/stories/readststory.html?storyID='

dictionary = {
    'title': 'Title:',
    'complete': 'Complete:',
    'categories': 'Categories:',
    'keywords': 'Key Words:',
    'age': 'Age:',
    'synopsis': 'Synopsis:',
    'rating': 'Rating:'
}

lists = ['categories', 'keywords']

def load_stories():
    with open('stories.json',) as f:
        return json.load(f)

def storyLinks(tag):
    return tag.name == 'a' and tag['href'].startswith('/stories/details.html')


def find_info(table, value):
    check = dictionary[value]
    for row in table.find_all('tr'):
        tds = row.find_all('td')

        if tds[0].text == check:
            if value in lists:
                list = []
                for item in tds[1].find_all('a'):
                    list.append(item.text)

                return list
            else:
                return tds[1].text


def get_stories_from_page(links, loaded_stories):
    stories = {}

    for link in links:
        story_url = DOMAIN+link['href']
        
        story = {}
        story['id'] = [int(s) for s in str.split(
            story_url, '=') if s.isdigit()][0]

        # print(load_stories[story])
        if str(story['id']) not in loaded_stories:
            story_page = requests.get(story_url)
            story_soup = BeautifulSoup(story_page.content, 'html.parser')
            story_table = story_soup.find('table')

            

            story['categories'] = find_info(story_table, 'categories')
            if 'Non-English story' in story['categories']:
                continue

            story['title'] = find_info(story_table, 'title')
            story['complete'] = find_info(story_table, 'complete')
            story['keywords'] = find_info(story_table, 'keywords')
            story['age'] = find_info(story_table, 'age')
            story['synopsis'] = find_info(story_table, 'synopsis')
            story['rating'] = find_info(story_table, 'rating')

            

            stories[story['id']] = story

        # download_story(story['id'])
    return stories


def get_page_results(start_from):
    print('start from ', start_from)
    URL = DOMAIN+SEARCH.format(start_from)
    page_data = requests.get(URL)

    page = BeautifulSoup(page_data.content, 'html.parser')

    # print(page)
    results = page.find_all(storyLinks)
    return results


start_from = 1
stories = load_stories()
# print(stories.keys())
while True:
    results = get_page_results(start_from)
    if len(results) == 0:  # or start_from > 1:
        break

    page_stories = get_stories_from_page(results, stories)

    if len(page_stories) == 0:
        print('BREAK')
        break

    stories.update(page_stories)

    # if len(page_stories) == 0:
    #     break

    start_from = start_from + 25

print(len(stories))

with open('stories.json', 'w') as outfile:
    json.dump(stories, outfile)

taxo = {}

taxo['categories'] = list({c for s in stories.values()
                           for c in s['categories']})
taxo['keywords'] = list({c for s in stories.values() for c in s['keywords']})
taxo['age'] = list({s['age'] for s in stories.values()})
taxo['complete'] = ['yes', 'no']
taxo['rating'] = ['X', 'XXX']

# print(taxo['categories'])

with open('taxo.json', 'w') as outfile:
    json.dump(taxo, outfile)
