import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
ff_options= Options()
ff_options.add_argument("--headless")     
driver = webdriver.Firefox(executable_path="/opt/homebrew/bin/geckodriver",options=ff_options)

DOMAIN = 'https://jav.guru/'
SUBBED = 'https://jav.guru/page/{}/'
MOVIESJSON = 'allmovies.json'
TAXOJSON = 'alltaxo.json'

def load_movies():
    with open(MOVIESJSON,) as f:
        return json.load(f)

def save_movies(movies):
    with open(MOVIESJSON, 'w') as outfile:
        json.dump(movies, outfile)

def get_page_results(page_number):
    print('--- Page: ', page_number, '---')
    URL = SUBBED.format(page_number)
    # print(URL)
    driver.get(URL)
    html = driver.page_source
    page = BeautifulSoup(html,'html.parser')

    # page_data = requests.get(URL)
    # page = BeautifulSoup(page_data.content, 'html.parser')

    # results = page.select("div.img > a")
    results = page.select("div.imgg > a:first-of-type")
    # print(page)
    # print(results)
    return results

def get_movie_data(link, loaded_movies):
    
    movie_url = link['href']
    url = movie_url.replace(DOMAIN, "")
    post_id = url[:url.find("/")]

    # print(movie_url, post_id, movie_id)
    
    if post_id in loaded_movies:
        return None, None
    
    movie = {}
    # movie['id'] = [int(s) for s in str.split(
    #     movie_url, '=') if s.isdigit()][0]

    # print(load_stories[story])
    driver.get(movie_url)
    html = driver.page_source
    story_soup = BeautifulSoup(html,'html.parser')

    # story_page = requests.get(movie_url)
    # story_soup = BeautifulSoup(story_page.content, 'html.parser')
    # print(story_soup)
    title = story_soup.title.string

    movie_id = title[title.find("[")+1:title.find("]")]

    movie['title'] = story_soup.select_one('h1.titl').text
    # movie['title'] = title[title.find(")")+1:].lstrip()

    print(movie['title'])
    print('>>>> ', movie_url)

    movie_info_left = story_soup.select_one('div.infoleft')

    page_tags = movie_info_left.select("a[href*='https://jav.guru/tag/']")
    movie['tags'] = sorted([a.text for a in page_tags], key=lambda v: v.upper()) if len(page_tags) > 0 else ['no tags']

    page_label = movie_info_left.select('a[href*="https://jav.guru/studio/"]')
    movie['label'] = [a.text for a in page_label][0] if len(page_label) > 0 else 'No Studio'
    
    page_studio = movie_info_left.select('a[href*="https://jav.guru/maker/"]')
    movie['studio'] = [a.text for a in page_studio][0] if len(page_studio) > 0 else 'No Studio'

    page_actress = movie_info_left.select('a[href*="https://jav.guru/actress/"]')
    movie['actress'] = sorted([a.text for a in page_actress], key=lambda v: v.upper()) if len(page_actress) > 0 else ['no actress']

    # page_date = movie_info_left[1]
    # movie['release_date'] = page_date.text.replace("Release Date: ", "")

    # page_tags = movie_info_left[3].find_all('a')
    # movie['tags'] = sorted([a.text for a in page_tags], key=lambda v: v.upper()) if len(page_tags) > 0 else ['no tags']

    # page_series = movie_info_left[4].find_all('a')
    # movie['series'] = [a.text for a in page_series][0] if len(page_series) > 0 else 'No Series'

    # page_actress = movie_info_left[5].find_all('a')
    # movie['actress'] = sorted([a.text for a in page_actress], key=lambda v: v.upper()) if len(page_actress) > 0 else ['no actress']

    # page_studio = movie_info_left[6].find_all('a')
    # movie['studio'] = [a.text for a in page_studio][0] if len(page_studio) > 0 else 'No Studio'
                
    cover = story_soup.select('div.large-screenimg > img')
    movie['cover'] = cover[0]['src']

    movie['url'] = movie_url

    time.sleep(1)
    # pprint(movie)
    # input("Press Enter to continue...")

    return post_id, movie


def get_movies_from_page(links, loaded_movies):
    movies = {}

    for link in links:
        try:
            post_id, movie = get_movie_data(link, loaded_movies)

            if post_id != None:
                movies[post_id] = movie

        except:
            try:
                post_id, movie = get_movie_data(link, loaded_movies)
                movies[post_id] = movie
                
                if post_id != None:
                    movies[post_id] = movie
                    
            except:
                post_id, movie = get_movie_data(link, loaded_movies)
                
                if post_id != None:
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

    if len(page_movies) > 0 and page_number % 5 == 0:
        save_movies(movies)

    page_number = page_number + 1



save_movies(movies)


taxo = {}
taxo['tags'] = list({c for s in movies.values() for c in s['tags']})
taxo['actress'] = list({c for s in movies.values() for c in s['actress']})
taxo['studio'] = list({s['studio'] for s in movies.values()})
taxo['label'] = list({s['label'] for s in movies.values()})

with open(TAXOJSON, 'w') as outfile:
    json.dump(taxo, outfile)

driver.quit()