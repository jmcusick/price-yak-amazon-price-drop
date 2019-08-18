import psycopg2
import logging
import sys
import argparse

from pgnotify import await_pg_notifications
from jmc.frugal.jmc_prices_db import api

def parse_args():
    parser = argparse.ArgumentParser(description='Monitor price drops for all ASINs')
    return parser.parse_args()

def setup_log():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def main():
    """Listen to channel prices from PostgresSQL database and print any price drops"""

    args = parse_args()
    setup_log()

    connection = psycopg2.connect(user='postgres',
                                  password='mysecretpassword',
                                  host='localhost',
                                  port='5432',
                                  database='my_postgres_db')

    channel = 'prices'

    logging.info('Listening for price drops on channel {}...'.format(channel))

    for notification in await_pg_notifications(
        connection,
        [channel]):

        logging.debug('Received notification on channel {} with payload {}'.format(notification.channel, notification.payload))

        asin = notification.payload

        last_two_offers = api.select_latest_offers(asin, 2)

        if not last_two_offers or len(last_two_offers) != 2:
            logging.debug('Could not find two records for asin {}'.format(asin))
            continue

        curr_price = last_two_offers[0]['price']
        curr_currency = last_two_offers[0]['currency']
        prev_price = last_two_offers[1]['price']
        prev_currency = last_two_offers[1]['currency']

        if curr_price < prev_price:
            curr_dollars = int(curr_price / 100)
            curr_cents = int(curr_price % 100)
            prev_dollars = int(prev_price / 100)
            prev_cents = int(prev_price % 100)
            logging.info('Price of {} dropped from ${}.{} {} to ${}.{} {}!'.format(asin, prev_dollars, prev_cents, prev_currency, curr_dollars, curr_cents, curr_currency))


if __name__ == '__main__':
    main()
