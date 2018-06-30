# Bubble Tea in California

The purpose of this project was to collect data regarding bubble tea shops in California and do some exploration around that data.
I acquired bubble tea business information using the YelpAPI and piped the data into a PostgreSQL database. Once the data was ingested,
I exported the data into two datasets (bubble_tea.csv and hours.csv within the csvs directory). These two datasets were used for some
data exploration in a Jupyter notebook (exploration.ipynb). Some plots and maps generated by the data exploration are stored in the html
and png directory.

## Getting Started

It's possible to set up your environment to insert bubble tea business information into a PostgreSQL database as well.

### Prerequisites

PostgreSQL, Python3, and a Yelp API key are required to run the code.
To download PostgreSQL, see https://www.postgresql.org/download/
To download Python, see https://www.python.org/getit/
For information regarding obtaining a Yelp API key, see https://www.yelp.com/developers/faq

### Installing

To install the required packages, run

```
pipenv install
```

To setup your PostgreSQL database (assuming localhost) with the required tables, functions, triggers, and views, run

```
psql -U <username> -f seed.sql
```

It's also possible to pass in a flag for host (-h) and port (-p) if running seed.sql on a different machine.

## Setup

Either export your Yelp API key to an environment variable named YELP_API_KEY or
change the value of the YELP_API_KEY variable in settings.py

Within settings.py, update the DATABASE variable to reflect your database credentials
(if running localhost, most likely only need to update the database password)

Right now, in settings.py, the STATE variable is set to CA for California.
However, it's possible to import bubble tea locations from other states by
setting the value of this variable to another state abbreviation.

It's also possible to import bubble tea business hour information into the database (stored in the hours table)
if the IMPORT_HOURS variable in settings.py is set to True.

## Importing Data

To begin importing data into your database, run

```
python bubble_tea.py
```

Please note that the Yelp API is limited to 25,000 API calls a day, so any attempted API calls after
will not return any data.

## Exporting Data

Running the following command will export the results of the bubble_tea_w_fips view to ./csv/bubble_tea.csv
and the bubble_tea_w_hours view to ./csv/hours.csv

```
psql -U <username> -f export.sql
```

However, it's possible to modify export.sql to export any dataset to any location by changing the SELECT statement and output path respectively.