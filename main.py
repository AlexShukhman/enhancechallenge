'''

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

page = urlopen('http://google.com')

soup = bs(page, 'html.parser')

body = soup.find('body').prettify()

print(body)
