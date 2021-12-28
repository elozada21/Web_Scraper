import requests
from bs4 import BeautifulSoup
import pprint


def sort_stories_by_votes(hn_list):
    return sorted(hn_list, key=lambda k: k['votes'], reverse=True)


def get_titles_and_subtext(page_num):
    payload = {'p': page_num}
    res = requests.get('https://news.ycombinator.com/news', params=payload)
    soup = BeautifulSoup(res.text, 'html.parser')
    pages = soup.select('.titlelink')
    subtext = soup.select('.subtext')
    return pages, subtext


def create_custom_hn(num_pages):
    hn = []
    i = 1
    while i < num_pages:
        sites, subtext = get_titles_and_subtext(i)

        for idx, item in enumerate(sites):
            title = sites[idx].getText()
            href = sites[idx].get('href', None)
            vote = subtext[idx].select('.score')
            if len(vote):
                points = int(vote[0].getText().replace(' points', ''))
                if points >= 100:
                    hn.append({'title': title, 'link': href, 'votes': points})
        i += 1
    return sort_stories_by_votes(hn)


pprint.pprint(create_custom_hn(3))
