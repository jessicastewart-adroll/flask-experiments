########################
###POSTGRES ON HEROKU###
########################

# $ heroku addons:add heroku-postgresql:dev # create database 
# $ heroku config # get db 
# $ heroku pg:promote COLOR_ADDRESS # promote 
# $ export DATABASE_URL=postgres://igbmgdydpoccwb:FSsI7MGeCMzYztZ8XQnnDYyAwL@ec2-54-225-115-77.compute-1.amazonaws.com:5432/d4bggmnom1j9rd # set DATABASE_URL as operating system variable 

## hello.py example 
# DATABASE_URL:               postgres://igbmgdydpoccwb:FSsI7MGeCMzYztZ8XQnnDYyAwL@ec2-54-225-115-77.compute-1.amazonaws.com:5432/d4bggmnom1j9rd
# HEROKU_POSTGRESQL_BLUE_URL: postgres://igbmgdydpoccwb:FSsI7MGeCMzYztZ8XQnnDYyAwL@ec2-54-225-115-77.compute-1.amazonaws.com:5432/d4bggmnom1j9rd

import urlparse # parses database url
import psycopg2 # connects python and postgres
import os # gets database url from os variable 

urlparse.uses_netloc.append("postgres") # add postgres as scheme
url = urlparse.urlparse(os.environ["DATABASE_URL"]) # get database url 

conn = psycopg2.connect("dbname={} user={} password={} host={} ".format(url.path[1:], url.username, url.password, url.hostname)) # use data from database url to connect to postgres
cur = conn.cursor() # create cursor 

cur.execute("CREATE TABLE Users(Id INTEGER PRIMARY KEY, Name VARCHAR(20))") # 1. create table 

cur.execute("INSERT INTO Users VALUES(1, 'jess')") # 2. insert row 

conn.commit() # 3. save change, COMMIT ON CONNECTION OBJECT

cur.execute("SELECT * FROM Users") # 4. get data from table

cur.fetchall() # 5. extract data from cursor, FETCH ON CURSOR OBJECT, output is LIST of TUPLES 

conn.close() # 6. close connection 
