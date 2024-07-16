class Listing:
    def __init__(self, url, seller_title, site_title, price):
        self.url = url
        self.seller_title = seller_title
        self.site_title = site_title
        self.price = price

    def __str__(self):
        return (f"url: {self.url}, "
                f"seller_title: {self.seller_title}, "
                f"site_title: {self.site_title}, "
                f"price: {self.price}")