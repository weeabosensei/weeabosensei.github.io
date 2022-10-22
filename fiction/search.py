import json
import io

html_head = """
<head>
<link rel="stylesheet" href="mystyle.css">
</head>
<html><div style='margin:0 auto;max-width:800px'>"""
html_footer = """</div></html>"""

story_print_format = """<h4>{title} - <a href=http://www.fictionmania.tv/stories/readtextstory.html?storyID={id}>link</a></h4>
<p><b>rating:</b> {rating} </p>
<p><b>cats:</b> {categories} </p>
<p><b>keywords:</b> {keywords} </p>
<p><b>age:</b> {age} </p>

<p>{synopsis}</p>
<hr>

"""


def load_taxo():
    with open('taxo.json',) as f:
        return json.load(f)


def load_stories():
    with open('stories.json',) as f:
        return json.load(f).values()


def print_menu(options):
    print(30 * '-')
    print("   MENU")
    print(30 * '-')
    for i in range(len(options)):
        print("{}. {}".format(i + 1, options[i]))
    print(30 * '-')


def get_options(options):
    options.sort()

    print_menu(options)
    ## Get input ###
    choice = input('Enter your choices: ')

    ### Convert string to int type ##
    choices = [int(s) for s in str.split(choice) if s.isdigit()]

    return [options[c-1] for c in choices]


def get_stories(categories, keywords, age, rating, other, text):
    all_stories = load_stories()
    stories = all_stories

    if len(categories) > 0:
        stories = [s for s in stories if all(
            story_taxo in s['categories'] for story_taxo in categories)]

    if len(keywords) > 0:
        stories = [s for s in stories if all(
            story_taxo in s['keywords'] for story_taxo in keywords)]

    if len(age) > 0:
        stories = [s for s in stories if s['age'] in age]

    if len(rating) > 0:
        stories = [s for s in stories if s['rating'] in rating]

    if len(other) > 0:
        stories = [s for s in stories if (
            s['title']+s['synopsis']).find(other) > -1]

    if len(text) > 0:
        terms = text.split(';')
        results = []
        for story in stories:
            # print(story['id'])
            try:
                with io.open('stories/{}.txt'.format(str(story['id'])), 'r',  encoding="ISO-8859-1") as f:
                    story_text = f.read()
                    if all(term in story_text for term in terms):
                        results.append(story)
            except:
                print('couldnt open: '+str(story['id']))
        return results

    return stories


def save_stories(stories):
    with open('results.html', 'w') as f:
        f.write(html_head)
        for story in stories:
            f.write(story_print_format.format(**story))
        f.write(html_footer)


taxo = load_taxo()

categories = get_options(taxo['categories'])
keywords = get_options(taxo['keywords'])
age = get_options(taxo['age'])
rating = get_options(taxo['rating'])
other = input('Search title, synopsis: ')
text = input('Search on story (; to separate): ')

print(categories, keywords, age, rating, other)
stories = get_stories(categories, keywords, age, rating, other, text)

print(len(stories))
save_stories(stories)
