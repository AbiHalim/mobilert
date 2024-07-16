import requests
from bs4 import BeautifulSoup

headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Safari/605.1.15"}

def olxscrape(query):
    print(f"Starting olx scraping: {query}")
    query.replace(" ", "+")  # fit url format
    site = requests.get(f"https://www.olx.co.id/items/q-{query}/", headers=headers)
    doc = BeautifulSoup(site.content, 'html.parser')

    print("Successfully retrieved olx page")

    olxlist = []

    listings = doc.find_all("li", class_="_3V_Ww")  # get all listings on page
    for listing in listings:
        # attach url to olx domain
        urltail = listing.find("a")["href"]
        url = f"https://www.olx.co.id+{urltail}/"

        # get site and seller title
        div = listing.find("div", class_="_2Gr10")
        seller_title = div["title"]
        site_title = div.get_text()

        # get price and strip non digit characters, convert to int
        raw_price = listing.find("span", class_="_1zgtX").get_text()
        price = int(''.join([char for char in raw_price if char.isdigit()]))

        finalisting = {"url":url, "seller_title":seller_title, "site_title":site_title, "price":price}
        print(finalisting)

        olxlist.append(finalisting)

    print(f"Finished olx scraping: {query}")
    return olxlist