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
import csv

# ***** Helpers *****


# Preliminary Setup
def setUp():
    with open('sites.csv', 'r') as f:
        reader = csv.reader(f)
        sites = list(reader)
    return sites


# Create Site Object from File
def readSite(site):
    with open('sites/' + site + '.html', 'r') as f:
        html = f.read()

    with open('csvs/' + site + '.csv', 'r') as f:
        breakdown = list(csv.reader(f))

    return Site(site, html, breakdown)


# ***** Site Class *****
class Site:
    def __init__(self, site, html=None, breakdown=None):
        self.site, self.html, self.breakdown = site, html, breakdown
        self.bs = None
        if html is None or breakdown is None:
            self._build()

    def _build(self):
        if self.html is None:
            self.html = urlopen(self.site)

        self.bs = bs(self.html, 'html.parser')

        if self.breakdown is None:
            teasers = self.bs.find_all(lambda tag: tag.name == "a" and
                                       tag.get("class") == ["teaser__link"])
            self.breakdown = []
            for teaser in teasers:
                img = teaser.find_all('img')
                if len(img) > 0:
                    imgSrc = img[0].get('src')
                else:
                    imgSrc = None
                self.breakdown.append((teaser.get('href'),
                                       teaser.get('aria-label'), imgSrc))
