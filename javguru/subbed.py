import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint

DOMAIN = 'https://jav.guru/'
SUBBED = 'https://jav.guru/category/english-subbed/page/{}/'

def load_movies():
    with open('movies.json',) as f:
        return json.load(f)

def get_page_results(page_number):
    print('Page: ', page_number)
    URL = SUBBED.format(page_number)
    # print(URL)
    page_data = requests.get(URL)

    page = BeautifulSoup(page_data.content, 'html.parser')

    results = page.select("div.imgg > a:first-of-type")
    # print(results)
    return results

def get_movies_from_page(links, loaded_movies):
    movies = {}

    for link in links:
        movie_url = link['href']
        
        movie = {}
        # movie['id'] = [int(s) for s in str.split(
        #     movie_url, '=') if s.isdigit()][0]

        # print(load_stories[story])
        story_page = requests.get(movie_url)
        story_soup = BeautifulSoup(story_page.content, 'html.parser')
    
        title = story_soup.title.string

        movie_id = title[title.find("[")+1:title.find("]")]
        url = movie_url.replace(DOMAIN, "")
        post_id = url[:url.find("/")]

        # print(movie_url, post_id, movie_id)
        
        if post_id not in loaded_movies:
            movie['title'] = story_soup.select_one('h1.titl').text
            # movie['title'] = title[title.find(")")+1:].lstrip()

            print(movie_id, movie['title'])

            movie_info_left = story_soup.select('div.infoleft > ul > li')
            
            page_date = movie_info_left[1]
            movie['release_date'] = page_date.text.replace("Release Date: ", "")

            page_tags = movie_info_left[3].find_all('a')
            movie['tags'] = sorted([a.text for a in page_tags], key=lambda v: v.upper()) if len(page_tags) > 0 else ['no tags']

            page_actress = movie_info_left[5].find_all('a')
            movie['actress'] = sorted([a.text for a in page_actress], key=lambda v: v.upper()) if len(page_actress) > 0 else ['no actress']

            page_studio = movie_info_left[6].find_all('a')
            movie['studio'] = [a.text for a in page_studio][0] if len(page_tags) > 0 else 'No Studio'
                      
            

            cover = story_soup.select('div.large-screenimg > img')
            movie['cover'] = cover[0]['src']

            movie['url'] = movie_url
            # pprint(movie)
            # input("Press Enter to continue...")
         
            movies[post_id] = movie

    return movies

page_number = 1

movies = load_movies()

while True:
    results = get_page_results(page_number)
    
    if len(results) == 0:
        break

    page_movies = get_movies_from_page(results, movies)

    if len(page_movies) == 0:
        print('BREAK')
        break

    movies.update(page_movies)

    page_number = page_number + 1

with open('movies.json', 'w') as outfile:
    json.dump(movies, outfile)


taxo = {}
taxo['tags'] = list({c for s in movies.values() for c in s['tags']})
taxo['actress'] = list({c for s in movies.values() for c in s['actress']})
taxo['studio'] = list({s['studio'] for s in movies.values()})

with open('taxo.json', 'w') as outfile:
    json.dump(taxo, outfile)
