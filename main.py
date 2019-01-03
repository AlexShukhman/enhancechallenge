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
import os


# ***** Site Class *****
class Site:
    def __init__(self, site, html=None, breakdown=None):
        self.site, self.html, self.breakdown = site, html, breakdown
        self.bs = None
        if html is None or breakdown is None:
            self._build()

        else:
            self._rebuild()

    def __repr__(self):
        return self.breakdown

    def __str__(self):
        return self.html

    def _build(self):
        if self.site in self._getSites():
            self._grab()

        else:
            if self.html is None:
                html = urlopen(self.site)
                self.bs = bs(html, 'html.parser')
                self.html = self.bs.prettify()

            else:
                self.bs = bs(self.html, 'html.parser')

            if self.breakdown is None:
                teasers = self.bs.find_all(lambda tag: tag.name == "a" and
                                           tag.get("class") ==
                                           ["teaser__link"])
                self.breakdown = []
                for teaser in teasers:
                    img = teaser.find_all('img')
                    if len(img) > 0:
                        imgSrc = img[0].get('src')
                    else:
                        imgSrc = None
                    self.breakdown.append((self.site + teaser.get('href'),
                                           teaser.get('aria-label'), imgSrc))
            self._save()

    def _grab(self):
        site = self._getSiteName()
        with open('sites/' + site + '.html', 'r') as f:
            self.html = f.read()

        with open('csvs/' + site + '.csv', 'r') as f:
            self.breakdown = list(csv.reader(f))

    def _rebuild(self):
        self.bs = bs(self.html, 'html.parser')
        self._save()

    def _save(self):
        site = self._getSiteName()
        with open('sites/' + site + '.html', 'w') as f:
            f.write(self.html)

        with open('csvs/' + site + '.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['href', 'desc', 'img href'])
            writer.writerows(self.breakdown)

        sites = self._getSites()
        if self.site not in sites:
            sites.append(self.site)
            with open('sites.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerow(sites)

    def _getSites(self):
        with open('sites.csv', 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            if len(rows) < 1:
                return []
            sites = rows[0]
        return sites

    def _getSiteName(self):
        site = self.site.split('/')
        if site[0] == 'http:' or 'https:':
            name = site[2]
        else:
            name = site[0]
        breakdown = name.split('.')
        return breakdown[-2] + '-homepage'

    def remove(self):  # to remove site from system
        sites = self._getSites()
        sites.remove(self.site)
        site = self._getSiteName()
        with open('sites.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(sites)
        os.remove('sites/' + site + '.html')
        os.remove('csvs/' + site + '.csv')


# ***** Main Function *****
def main(site):
    economist = Site(site)
    return economist.__repr__()


if __name__ == "__main__":
    main("https://www.economist.com/")
