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
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def main():
    """Scrape prices from Amazon and upload them to a PostgreSQL database"""

    args = parse_args()
    setup_log()

    while True:

        min_priced_offer = price_scraper.get_cheapest_offer(args.asin)

        api.insert_offer(min_priced_offer)

        time.sleep(args.wait)

if __name__ == '__main__':
    main()
