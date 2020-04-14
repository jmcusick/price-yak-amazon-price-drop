FROM postgres:12

COPY ./init.sql /docker-entrypoint-initdb.d/init.sql

# default password that can be overriden when building the image
ARG buildtime_postgres_pw=mysecretpassword
ENV POSTGRES_PASSWORD=$buildtime_postgres_pw 

# already done by postgres:12
EXPOSE 5432
