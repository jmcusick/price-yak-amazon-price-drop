class Offer:
    def __init__(
        self,
        asin,
        offer_id,
        seller_id,
        seller_name,
        price,
        currency,
        access_timestamp
    ):
        self.asin = asin
        self.offer_id = offer_id
        self.seller_id = seller_id
        self.seller_name = seller_name
        self.price = price
        self.currency = currency
        self.access_timestamp = access_timestamp