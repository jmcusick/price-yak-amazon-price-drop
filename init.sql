CREATE DATABASE my_postgres_db OWNER postgres;
\c my_postgres_db
CREATE TABLE prices (
    asin varchar(32) NOT NULL,
    offer_id varchar(256),
    seller_id varchar(32),
    seller_name varchar(256),
    price int,
    currency varchar(32),
    access_timestamp int NOT NULL,
    PRIMARY KEY(asin, access_timestamp)
);
