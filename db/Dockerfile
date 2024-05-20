FROM postgres:15.6

# Creating dirs for archives
COPY ./init.sql /docker-entrypoint-initdb.d/init.sql.raw
USER postgres
