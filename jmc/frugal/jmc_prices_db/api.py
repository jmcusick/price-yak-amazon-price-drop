import logging
import psycopg2
import psycopg2.extras
import os

from contextlib import closing
from jmc.frugal.jmc_prices_db.data import Offer

def select_latest_offers(asin, n):
    """Return a dictionary of the latest n cheapest offers from the database

    :return: a list of dictionaries keyed by the column name
    """

    connection = None
    cursor = None
    try:
        with closing(psycopg2.connect(user='postgres',
                                      password='mysecretpassword',
                                      host=os.environ['JMC_PRICE_YAK_DB_SERVICE_HOST'],
                                      port=os.environ['JMC_PRICE_YAK_DB_SERVICE_PORT'],
                                      database='my_postgres_db')) as connection:

            with closing(connection.cursor(cursor_factory=psycopg2.extras.DictCursor)) as cursor:

                postgresql_select_query = 'SELECT * FROM prices WHERE asin = %s ORDER BY access_timestamp DESC LIMIT %s'
                params = (asin, n)

                cursor.execute(postgresql_select_query, params)

                offers = cursor.fetchall()

                return offers

    except (Exception, psycopg2.Error) as error :
        logging.error('Error while fetching data from PostgreSQL', error)


def insert_offer(offer):
    """Insert an offer into the database and notify listeners

    :param Offer offer: The offer to insert
    """

    connection = None
    try:
        with closing(psycopg2.connect(user='postgres',
                                      password='mysecretpassword',
                                      host=os.environ['JMC_PRICE_YAK_DB_SERVICE_HOST'],
                                      port=os.environ['JMC_PRICE_YAK_DB_SERVICE_PORT'],
                                      database='my_postgres_db')) as connection:
            with closing(connection.cursor()) as cursor:

                postgresql_insert_query = 'INSERT INTO prices (asin, offer_id, seller_id, seller_name, price, currency, access_timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s)'
                values = (
                    offer.asin,
                    offer.offer_id,
                    offer.seller_id,
                    offer.seller_name,
                    offer.price,
                    offer.currency,
                    offer.access_timestamp
                )

                cursor.execute(postgresql_insert_query, values)

                postgresql_notify_query = 'NOTIFY prices, %s'
                payload = (offer.asin,)
                cursor.execute(postgresql_notify_query, payload)

                connection.commit()

                count = cursor.rowcount
                logging.debug('Inserted {} rows'.format(count))

                if count:
                    logging.info('Inserted offer for {} at ${}.{} {}'.format(offer.asin, int(offer.price/100), int(offer.price%100), offer.currency))

    except (Exception, psycopg2.Error) as error :
        logging.error('Error while inserting data into PostgreSQL', error)
