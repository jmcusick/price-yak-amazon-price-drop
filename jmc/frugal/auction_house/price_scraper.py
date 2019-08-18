import requests
import logging

from jmc.frugal.jmc_prices_db.data import Offer

def get_cheapest_offer(asin):
    """Scrape offers for a given ASIN and return the cheapest one"""

    token='B9DD68C645191A9DD0E57556'
    url='https://api.zinc.io/v1/products/{}/offers'
    retailer='amazon'

    params = {'retailer':retailer, 'max_age': 30}

    r = requests.get(url = url.format(asin), params = params, auth = (token,''))

    data = r.json()

    logging.debug(data)

    # We only care about the cheapest order
    min_priced_offer = min(data['offers'], key=lambda x:x['price'])

    return Offer(
        min_priced_offer['asin'],
        min_priced_offer['offer_id'],
        min_priced_offer['seller']['id'],
        min_priced_offer['seller']['name'],
        min_priced_offer['price'],
        min_priced_offer['currency'],
        data['timestamp']
    )
