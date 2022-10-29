import os
import psycopg2


URI = "postgres://ntenniladwleew:6e46f4a1e4c6ae7d1504a49e88cbf0ccf3cc9a77c51e0766fb35a410a1d38f67@ec2-3-214-2-141.compute-1.amazonaws.com:5432/d4fib2msl3p018"
## set uri as environment variable
# DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(URI, sslmode='require')
# print("true")