import requests
from bs4 import BeautifulSoup

headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Safari/605.1.15"}

def mobil123scrape(query):
    print(f"Starting mobil123 scraping: {query}")
    query.replace(" ", "+")  # fit url format
    site = requests.get(f"https://www.mobil123.com/mobil-dijual/indonesia?keyword={query}/", headers=headers)
    doc = BeautifulSoup(site.content, 'html.parser')

    print("Successfully retrieved mobil123 page")

    mobil123list = []

    listings = doc.find_all("article", class_="listing")
    for listing in listings:
        url = listing.get("data-url")

        seller_title = listing.get("data-title")

        site_title = listing.get("data-display-title")

        line_text = listing.get("data-default-line-text")

        #  remove non digit characters from price and convert to int
        raw_price = line_text.split(" ")[-2]
        price = int(''.join([char for char in raw_price if char.isdigit()]))

        finalisting = {"url":url, "seller_title":seller_title, "site_title":site_title, "price":price}
        print(finalisting)

        mobil123list.append(finalisting)

    print(f"Finished mobil123 scraping: {query}")
    return mobil123list