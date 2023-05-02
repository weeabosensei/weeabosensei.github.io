import requests
import json
import os
from tqdm import tqdm
from pprint import pprint
import time
import re
import frontmatter
import ruamel.yaml
yaml = ruamel.yaml.YAML()

DOMAIN = 'http://fictionmania.tv'
SEARCH = '/searchdisplay/ratingdisplay.html?startat={}&rate=X'
# https://www.fictionmania.tv/stories/readststory.html?storyID=1611943084142133846
DOWNLOAD = '/stories/readststory.html?storyID='

MAIN_DIR = '/Users/thiago/git/things/P/fictionmania/stories'
LIMIT = 500

# def extract_number(f):
#     s = re.findall("\d+$",f)
#     return (int(s[0]) if s else -1,f)

# print(max(list_of_files,key=extract_number))
def get_new_folder():
    folderNumber = 0

    for path in os.listdir(MAIN_DIR):
        # check if current path is a file
        if not os.path.isfile(os.path.join(MAIN_DIR, path)):
            num = int(path)
            if num > folderNumber:
                folderNumber = num
            # res.append(path)

    if folderNumber == 0:
        return os.path.join(MAIN_DIR, str(1))
    
    dir_path = os.path.join(MAIN_DIR, str(folderNumber))
    folder_size = len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))])
    
    if folder_size >= LIMIT:
        folderNumber += 1

    return os.path.join(MAIN_DIR, str(folderNumber))

def load_md():
    story_data = {}
    story_files = {}

    for root, dirs, files in os.walk(MAIN_DIR, topdown=False):
        for name in files:
            try:
                file_path = os.path.join(root, name)
                if file_path.endswith('.DS_Store') or file_path.startswith('{}/Inbox/'.format(MAIN_DIR)):
                    continue

                # print(file_path)
                data = frontmatter.load(file_path)
                # print('\n\n\n------\n')
                # pprint(data.metadata)
                # pprint(data.content)

                story_data[str(data.metadata['storyId'])] = data
                story_files[str(data.metadata['storyId'])] = file_path
                # break
                # with open(file_path, 'r') as f:
                #     data = yaml.load_all(f)
                #     for itm in data:
                #         pprint(itm)
                #     break
                # stuff
            # for name in dirs:
            #     print(os.path.join(root, name))
                # stuff
            except:
                print("EXCEPT: ", file_path)
                raise Exception("stop")

    return story_data, story_files

def getFilename(story):
    fn = '{} - {}'.format(story['id'], story['title'])
    return fn.translate({ord(i): None for i in '\:#[]|""/'}).replace('  ', ' ').strip()

def cleanTag(tag):
    return tag.replace(' / ','--').replace(' & ', '--').replace(' ','-')

def getTags(keyword, items):
    return ['{}/{}'.format(keyword, cleanTag(item)) for item in items]

def file_frontmatter(data):
    tags = []
    tags.extend(getTags('fictionMania/category',data['categories']))
    tags.extend(getTags('fictionMania/keyword',data['keywords']))
    tags.append('fictionMania/age/{}'.format(cleanTag(data['age'])))
    tags.append('fictionMania/rating/{}'.format(data['rating']))

    frontmatter = {}
    frontmatter['tags'] = tags
    frontmatter['storyId'] = data['id']

    return frontmatter

def get_extra(story):
    text = """{synopsis}
***

"""

    return text.format(**story)    

def load_stories():
    with open('stories.json',) as f:
        return json.load(f)


def download_story(story, existingFile):
    id = story['id']
    url = DOMAIN + DOWNLOAD + str(id)
    # try:
    # storyReq = requests.get(url)
    
    # if storyReq.ok == False:
    #     return 
    
    content = ''
    frontmatterData = file_frontmatter(story)
    frontmatterData['url'] = url

    # if storyReq.text.find('<title>429 Too Many Requests</title>'):
    #     if existingFile != None and existingFile != '':
    #         raise Exception('too many requests')
        # print(storyReq.content)
        # raise Exception('too many requests')
    frontmatterData['downloaded'] = False
    # else:
    #     content = storyReq.text
    #     frontmatterData['downloaded'] = True
    
    folder = get_new_folder()
    fn = getFilename(story)

    if not os.path.exists(folder):
        os.makedirs(folder)

    with open('{}/{}.md'.format(folder,fn), 'w') as outfile:
        outfile.write('---\n')
        yaml.dump(frontmatterData, outfile)
        outfile.write('---\n')
        extra_data = get_extra(story)
        outfile.write(extra_data)
        outfile.write(content)
    # except:
    #     print("unable to download story " + str(id))

stories = load_stories()
all_ids = stories.keys()


# for id in all_ids:
for id in tqdm(all_ids):
    # folder = storyFolder(int(id))
    # fn = getFilename(stories[id])
    # isExist = os.path.exists(folder)

    # if not isExist:
    #     os.makedirs(folder)

    # if os.path.isfile('{}/{}.md'.format(folder,fn)):
    #     continue

    # print('a')
    download_story(stories[id], '')
    time.sleep( 1 )
