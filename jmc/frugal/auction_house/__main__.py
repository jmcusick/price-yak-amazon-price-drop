import argparse
import logging
import sys
import time

from jmc.frugal.auction_house import price_scraper
from jmc.frugal.jmc_prices_db import api

def parse_args():
    parser = argparse.ArgumentParser(description='Periodically grab Amazon pricing data')
    parser.add_argument('-a', '--asin', dest='asin', required=True,
                        help='the Amazon Standard Identification Number of the prodct to track')
    parser.add_argument('-w', '--wait', dest='wait', type=int, default=30, choices=[30, 60, 300],
                        help='the number of seconds to wait between price queries (default: 30s)')
    return parser.parse_args()

def setup_log():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def main():
    args = parse_args()
    setup_log()

    while True:

        min_priced_offer = price_scraper.get_cheapest_offer(args.asin)

        asin = min_priced_offer['asin']
        offer_id = min_priced_offer['offer_id']
        seller_id = min_priced_offer['seller']['id']
        seller_name = min_priced_offer['seller']['name']
        price = min_priced_offer['price']
        currency = min_priced_offer['currency']
        timestamp = min_priced_offer['timestamp']

        print(offer_id)
        print(seller_id)
        print(seller_name)
        print(price)
        print(currency)

        api.insert_offer(asin, price, timestamp)

        time.sleep(args.wait)

if __name__ == "__main__":
    main()
