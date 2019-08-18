import psycopg2
import psycopg2.extras

from contextlib import closing

def select_latest_offers(asin, n):
    connection = None
    cursor = None
    try:
        with closing(psycopg2.connect(user='postgres',
                                      password='mysecretpassword',
                                      host='localhost',
                                      port='5432',
                                      database='postgres')) as connection:

            with closing(connection.cursor(cursor_factory=psycopg2.extras.DictCursor)) as cursor:

                postgresql_select_query = 'SELECT * FROM prices WHERE asin = %s ORDER BY access_timestamp DESC LIMIT %s'
                params = (asin, n)

                cursor.execute(postgresql_select_query, params)

                offers = cursor.fetchall()

                column_names = [desc[0] for desc in cursor.description]

                return offers

    except (Exception, psycopg2.Error) as error :
        print('Error while fetching data from PostgreSQL', error)


def insert_offer(asin, price, timestamp):

    connection = None
    try:
        connection = psycopg2.connect(user='postgres',
                                      password='mysecretpassword',
                                      host='localhost',
                                      port='5432',
                                      database='postgres')
        cursor = connection.cursor()

        postgresql_insert_query = 'INSERT INTO prices (asin, price, access_timestamp) VALUES (%s,%s,%s)'
        values = (asin, price, timestamp)

        cursor.execute(postgresql_insert_query, values)

        postgresql_notify_query = 'NOTIFY prices, %s'
        payload = (asin,)
        cursor.execute(postgresql_notify_query, payload)

        connection.commit()

        count = cursor.rowcount

        print('Inserted {} rows'.format(count))

    except (Exception, psycopg2.Error) as error :
        print ('Error while inserting data into PostgreSQL', error)
    finally:
        #closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print('PostgreSQL connection is closed')
