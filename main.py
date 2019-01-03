''' Python Version 3.6.1

Enhance Coding Challenge
Alex Shukhman

'''
# Imports
from bs4 import BeautifulSoup as bs
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

page = urlopen('http://www.economist.com')

soup = bs(page, 'html.parser')

teasers = soup.find_all(lambda tag: tag.name == "a" and tag.get("class") == ["teaser__link"])

teaserInfos = []

for teaser in teasers:
    img = teaser.find_all('img')
    if len(img) > 0:
        imgSrc = img[0].get('src')
    else: 
        imgSrc = None
    teaserInfos.append((teaser.get('href'), teaser.get('aria-label'), imgSrc))

for info in teaserInfos:
    print(info)
