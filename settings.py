import os

# API key needed to use the Yelp API
YELP_API_KEY = os.environ['YELP_API_KEY']

# Used to define and create database URL
DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'postgres',
    'password': os.environ['POSTGRES_DB_PASSWORD'],
    'database': 'bubble_tea'
}

# State to import bubble tea location info
STATE = 'CA'

# Import bubble tea business hour info if set to True
# Set to False by default.
IMPORT_HOURS = False
