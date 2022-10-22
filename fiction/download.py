import requests
import json
import os
from tqdm import tqdm

DOMAIN = 'http://fictionmania.tv'
SEARCH = '/searchdisplay/ratingdisplay.html?startat={}&rate=X'
# https://www.fictionmania.tv/stories/readststory.html?storyID=1611943084142133846
DOWNLOAD = '/stories/readststory.html?storyID='


def load_story_ids():
    with open('stories.json',) as f:
        return json.load(f).keys()


def download_story(id):
    url = DOMAIN + DOWNLOAD + str(id)
    try:
        story = requests.get(url)
        with open('stories/{}.txt'.format(str(id)), 'wb') as outfile:
            outfile.write(story.content)
    except:
        print("unable to download story " + str(id))


all_ids = load_story_ids()

for id in tqdm(all_ids):
    if os.path.isfile('stories/{}.txt'.format(str(id))):
        continue
    download_story(id)
