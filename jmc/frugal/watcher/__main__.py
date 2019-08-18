import psycopg2
import logging
import sys

from pgnotify import await_pg_notifications
from jmc.frugal.jmc_prices_db import api

# def parse_args():
#     parser = argparse.ArgumentParser(description='Process some integers.')
#     parser.add_argument('-a', '--asin', dest='asin', required=True,
#                         help='the Amazon Standard Identification Number of the prodct to track')
#     parser.add_argument('-w', '--wait', dest='wait', type=int, default=30, choices=[30, 60, 300],
#                         help='the number of seconds to wait between price queries (default: 30s)')
#     return parser.parse_args()

def setup_log():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def main():
#    args = parse_args()
    setup_log()

    connection = psycopg2.connect(user='postgres',
                                  password='mysecretpassword',
                                  host='localhost',
                                  port='5432',
                                  database='postgres')

    for notification in await_pg_notifications(
        connection,
        ['prices']):

        print(notification.channel)
        print(notification.payload)

        asin = notification.payload

        last_two_offers = api.select_latest_offers(asin, 2)

        if not last_two_offers or len(last_two_offers) != 2:
            logging.debug('Could not find two records for asin {}'.format(asin))
            continue

        curr_price = last_two_offers[0]['price']
        prev_price = last_two_offers[1]['price']

        if curr_price < prev_price:
            curr_dollars = int(curr_price / 100)
            curr_cents = int(curr_price % 100)
            prev_dollars = int(prev_price / 100)
            prev_cents = int(prev_price % 100)
            print('Price of {} from ${}.{} to ${}.{}'.format(asin, prev_dollars, prev_cents, curr_dollars, curr_cents))


if __name__ == "__main__":
    main()
