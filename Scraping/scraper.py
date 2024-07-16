from Scraping.mobil123 import mobil123scrape
from Scraping.olx import olxscrape

def scrape(query):
    mobil123list = mobil123scrape(query)
    olxlist = olxscrape(query)

    finalist = mobil123list + olxlist

    print(finalist)
    return finalist