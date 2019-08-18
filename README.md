[![Build Status](http://jenkins.jmorgancusick.com/buildStatus/icon?job=jmorgancusick%2Fprice-yak-amazon-price-drop%2Fmaster)](http://jenkins.jmorgancusick.com/job/jmorgancusick/job/price-yak-amazon-price-drop/job/master/)

# price-yak-amazon-price-drop aka Frugal
A price watcher that notifies you of sudden price drops for an Amazon product (example product B00FE2N1WS).

Frugal is an application comprised of three parts:

* A price scraper (aka auction_house) that calls [Zincs Data API](https://docs.zincapi.com/#product-offers) and uploads _minimum price data_ (only the lowest offer) to a database for a single product
* A listener (aka watcher) that listens for price changes across all products from said database and outputs a message if any prices drop
* A PostgreSQL database which serves as the medium between the two

This application leverages my personal [Jenkins CI webserver](http://jenkins.jmorgancusick.com) for [pytest](https://docs.pytest.org/en/latest/) unit testing. It uses [docker-compose](https://docs.docker.com/compose/) for container orchestration and [pipenv](https://docs.pipenv.org/en/latest/) for python package management.

# How to run this application

**You must [install Docker](https://docs.docker.com/install/) in order to run this application**

After installing docker and cloning the repo, use tmux or open up several terminal windows and cd into the project's root directory. You will need 6 windows in total.

* In terminal 1: Start the postgresql database

~~~
docker-compose up postgresql
~~~

* In terminal 2: Start the price drop watcher

**This is where price notifications will be printed**

~~~
docker-compose up watcher
~~~

* In terminal 3: Start a price scraper for product [B07S9QS781](https://www.amazon.com/-/dp/B07S9QS781)

~~~
docker-compose run scraper bash -c "pipenv install && PYTHONPATH=. pipenv run python3 ./jmc/frugal/auction_house/__main__.py --asin B07S9QS781"
~~~

* In terminal 4: Start a second price scrape for product [B07F3GN2R1](https://www.amazon.com/-/dp/B07F3GN2R1)

~~~
docker-compose run scraper bash -c "pipenv install && PYTHONPATH=. pipenv run python3 ./jmc/frugal/auction_house/__main__.py --asin B07F3GN2R1"
~~~

* In terminal 5: Connect to the PostgreSQL database

~~~
docker-compose exec postgresql psql my_postgres_db -U postgres
SELECT * FROM prices ORDER BY access_timestamp DESC;
~~~

At this point, you should see offers being uploaded by the scrapers in terminal windows 3 and 4 and rows in the database in terminal 5. If a live price drop where to happen, you'd see that ouputted by the watcher in terminal 2. 

Let's artificially drop one of the product's prices and see that notification. In the psql prompt in terminal 5, run the following query. This query takes the latest price of [B07S9QS781](https://www.amazon.com/-/dp/B07S9QS781), adds 1 second to the timestamp and removes 10 cents from the price:

~~~
INSERT INTO prices (asin, price, currency, access_timestamp) SELECT asin, price-10, currency, access_timestamp+1 FROM prices WHERE asin='B07S9QS781' ORDER BY access_timestamp DESC LIMIT 1; NOTIFY prices, 'B07S9QS781';
~~~

Switch to the watcher in window 2 and you should see a price drop log! You can run the above sql command multiple times for multiple price drops. You could also alter the above SQL query and replace both instances of ```B07S9QS781``` with ```B07F3GN2R1``` to witness a price drop for the other product that window 4 is scraping.

* In terminal 6: Tear everything down

Once you are done running, use the following command to tear down all containers:

~~~
docker-compose down
~~~
