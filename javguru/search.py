import json
import io

html_head = """
<head>
<link rel="stylesheet" href="mystyle.css">
<script>
    var val = 0;

    document.addEventListener('keydown', function (event) {
    if (event.keyCode === 37 || event.keyCode === 39) {
        if (event.keyCode === 37) val--;
        if (event.keyCode === 39) val++;
        console.log(val);
        var divsToHide = document.getElementsByClassName("movie"); //divsToHide is an array
            for(var i = 0; i < divsToHide.length; i++){
                // divsToHide[i].style.visibility = "hidden"; // or
                divsToHide[i].style.display = "none"; // depending on what you're doing
            }    
        
            var x = document.getElementById(""+val);
            console.log(x);
            x.style.display = "block";

    }
});
       
</script>
</head>
<html><div>


"""
html_footer = """</div></html>"""

story_print_format = """
<div id={number} class="movie">
<div style='margin:0 auto;max-width:1200px'>
<h2>{number}/{total}: <a href="{url}">{title}</a></h4>
<b>tags:</b> {tag_list} <br>
<b>actress:</b> {actress_list} <br>
<b>studio:</b> {studio} <br>
<b>release date:</b> {release_date} <br>
</div>
<img src="{cover}"/>
</div>

"""


def load_taxo():
    with open('taxo.json',) as f:
        return json.load(f)


def load_stories():
    with open('movies.json',) as f:
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


def get_stories(tags, actress, studio, other):
    all_stories = load_stories()
    stories = all_stories

    if len(tags) > 0:
        stories = [s for s in stories if all(
            story_taxo in s['tags'] for story_taxo in tags)]

    if len(actress) > 0:
        stories = [s for s in stories if all(
            story_taxo in s['actress'] for story_taxo in actress)]

    if len(studio) > 0:
        stories = [s for s in stories if all(
            story_taxo in s['studio'] for story_taxo in studio)]

    if len(other) > 0:
        stories = [s for s in stories if (
            s['title']).find(other) > -1]

    return stories

def save_stories(stories):
    total = len(stories)
    with open('results.html', 'w') as f:
        f.write(html_head)
        idx = 0
        for story in stories:
            idx+=1
            f.write(story_print_format.format(**story, number = idx, total=total, tag_list=", ".join(story["tags"]), actress_list=", ".join(story["actress"])))
        f.write(html_footer)


taxo = load_taxo()

tags = get_options(taxo['tags'])
actress = get_options(taxo['actress'])
studio = get_options(taxo['studio'])

other = input('Search title, synopsis: ')
# text = input('Search on story (; to separate): ')

# print(categories, keywords, age, rating)
# print(categories, keywords, age, rating, other)
stories = get_stories(tags, actress, studio, other)

print(len(stories))
save_stories(stories)
