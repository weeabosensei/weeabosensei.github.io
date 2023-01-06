from os import stat
from bs4 import BeautifulSoup
import requests
# import json, datetime, csv
from pprint import pprint
from datetime import datetime, date
import frontmatter
from io import BytesIO
import ruamel.yaml
from tqdm import tqdm

def selectonetext(page, label):
    itm = page.select_one(label)
    return itm.text if itm else None

def getText(item):
    if item and item.text != 'Unknown':
        return item.text.strip()

    return None

def getSlug(link):
    parts = link.split("/")
    # print(parts[-2])
    return parts[-2]

def toInt(number):
    if number:
        return int(number)

    return None

def getExtra(star):
    text = """country: [[{country}]]
![photo]({photo})
***

"""


    return text.format(**star)


with open("stars.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    # print(soup)

bios = soup.select('a[href*="/bio"]')
# bios = []

# print(len(bios))

stars = []

for bio in tqdm(bios):
    url = bio['href']

    page_data = requests.get(url)
    page = BeautifulSoup(page_data.content, 'html.parser')

    star = {}
    img = page.select_one("body > div.flex-footer-wrapper > div > div.right-container.flex-m-column.d-m-flex.flex-1 > main > div.px-2.px-md-3 > section > header > div.dashboard-image-container > a > img")
    star["name"] = img["title"].strip() if img else 'NO-NAME'
    star["photo"] = img["src"].strip() if img else None
    # pi = page.select_one('div[data-test="section-personal-information"]')
    pi = page.select_one('form[name="subject"]')
    # pprint(pi)

    dob = pi.select_one('span[data-test="link_span_dateOfBirth"]')
    birthday = dob.text.strip() if dob else None
    # star["birthday"] = datetime.strpt(birthday, "%B %d, %Y") if birthday else None
    star["birthday"] = datetime.strptime(birthday, "%B %d, %Y").strftime("%Y-%m-%d") if birthday else None #.strftime("%Y-%m-%d") if birthday else None
    # print(bday)
    # star["birthday"] = "{}-{}-{}".format(bday.year, bday.month, bday.day) if bday else None


    star["country"] = getText(pi.select_one('a[href*="/babes?f%5Bcountry%5D"]'))

    star["ethnicity"] = getText(page.select_one('span[data-test="link_span_ethnicity"]'))
    aliases = page.select('span[data-test="link_span_aliases"]')
    star["aliases"] = [alias.text.strip() for alias in aliases] if aliases else []

    # official website
    # links

    #appearance
    # appearance = page.select_one('ul.profile-meta-list')

    height = pi.select_one('span[data-test="link_span_height"]')
    star["height"] = toInt(height.text.strip().split(' - ')[0].split(' ')[0]) if (height and height.text != 'Unknown') else None

    weight = pi.select_one('span[data-test="link_span_weight"]')
    star["weight"] = toInt(weight.text.strip().split(' - ')[0].split(' ')[0]) if (weight and weight.text != 'Unknown') else None

    star["boobs"] = getText(pi.select_one('span[data-test="link_span_boobs"]'))
    star["bust"] = toInt(getText(pi.select_one('span[data-test="link_span_bust"]')))
    star["cup"] = getText(pi.select_one('span[data-test="link_span_cup"]'))
    star["bra"] = getText(pi.select_one('span[data-test="link_span_bra"]'))
    star["waist"] = toInt(getText(pi.select_one('span[data-test="link_span_waist"]')))
    star["hip"] = toInt(getText(pi.select_one('span[data-test="link_span_hip"]')))
    star["butt"] = getText(pi.select_one('span[data-test="link_span_butt"]'))
    star["eyes"] = getText(pi.select_one('span[data-test="link_span_eye_color"]'))
    star["hair"] = getText(pi.select_one('span[data-test="link_span_hair_color"]'))

    star["piercings"] = getText(pi.select_one('span[data-test="link_span_piercings"]'))
    star["piercingLocations"] = getText(pi.select_one('span[data-test="link_span_piercingLocations"]'))

    star["tattoos"] = getText(pi.select_one('span[data-test="link_span_tattoos"]'))
    star["tattooLocations"] = getText(pi.select_one('span[data-test="link_span_tattooLocations"]'))

    star["status"] = getText(page.select_one('span[data-test="link_span_careerStatus"]'))
    
    star['started'] = toInt(getText(pi.select_one("span[data-test='link_span_careerStart']")))

    star['until'] = toInt(getText(pi.select_one("span[data-test='link_span_careerEnd']")))

    social_urls = page.select('div.social-meta a')

    # pprint(social_urls)

    # star["Social"] = [a['href'] for a in social_urls]
    star["link"] = url

    # pprint(star)
    # if 'eva-elfie' in url:
    #     pprint(star)

    stars.append(star)
    # break

# def compare_data(notion_data, trakt_data):
#     TO_COMPARE = ['Name','Photo','Birthday','Country','Ethnicity','Aliases',
#     'Height','Weight','Boobs', 'Bust', 'Cup', 'Bra',
#     'Waist','Hip','Butt','Tattoos', 'Tattoo Locations','Piercings','Piercing Locations',
#     'Status','Started','Until'] # 'Eyes', 'Social'

#     stored = notion.get_props_data(notion_data)
#     to_update = {}
    
#     for key in TO_COMPARE:
#         notion_val = stored.get(key)
#         fo_val = trakt_data.get(key)
#         if fo_val != None and notion_val != fo_val:
#             # print(key, notion_val, trakt_val)
#             # pprint(notion)
#             # input('a')
#             to_update[key] = fo_val

#     return to_update

# notion_data = notion.get_notion_data("FREEONES")
# act_notion = format_notion_data(notion_data)

# pprint(act_notion)
yaml = ruamel.yaml.YAML()
# text_format = """---
# {}
# ---
# """
# yaml.explicit_start = True
# yaml.explicit_end = True
for star in stars:
    # pprint(star)
    # with open("{}.md".format(star["name"]), "wb") as f:
    # frontmatter.dump(star, "{}.md".format(star["name"]))
    with open("stars/{}.md".format(star["name"]), 'w') as fh:
        fh.write('---\n')
        yaml.dump(star, fh)
        fh.write('---\n')
        extra_data = getExtra(star)
        fh.write(extra_data)
        # fh.write(text_format.format(yaml.dump(star, sys.stdout)))

    # TODO: update or create
    # slug = getSlug(star['Link'])
    # if slug in act_notion:
    #     update_record(act_notion[slug], star)
    # else:
    #     # star['Photo'] = get_trakt_banner(trakt)
    #     print('insert')
    #     pprint(star)
    #     notion.insert_notion("FREEONES", star)

# csv_columns = ['Name','Photo','Birthday','Country','Ethnicity','Aliases','Eyes','Hair','Height','Weight','Bra','Waist','Hip','Boobs','Shoes','Tattoos','Piercings','Status','Started','Until','Social','Freeones']
# time_stamp =  datetime.datetime.now().strftime("%b-%d-%y-%H:%M:%S")

# with open('stars_{}.csv'.format(time_stamp), mode='w') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#     writer.writeheader()
#     for data in stars:
#         writer.writerow(data)




# def yaml(self):
#         logs_list = None
#         if self.logs is not None:
#             logs_list = [lm.yaml() for lm in self.logs]

#         data = OrderedDict([
#             ('service_name', self.name),
#             ('team_name', self.team_name),
#             ('port', self.port),
#             ('healthcheck_url', self.healthcheck_url),
#             ('logs', logs_list),
#             ('code_deploy_logs', self.code_deploy_logs),
#             ('environments', [e.yaml() for e in self.environments])
#         ])
#         return pyaml.dump(OrderedDict((k, v) for k, v in data.items() if v is not None)) 