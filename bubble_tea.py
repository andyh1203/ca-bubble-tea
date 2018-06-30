import requests

from sqlalchemy.orm import sessionmaker

from models import BubbleTea, db_connect, ZipCode
from settings import IMPORT_HOURS, STATE, YELP_API_KEY


api_url = 'https://api.yelp.com/v3/graphql'

headers = {
    'Authorization': 'Bearer {}'.format(YELP_API_KEY),
    'Content-Type': 'application/json'
}

# GraphQL search query
# (see https://www.yelp.com/developers/graphql/query/search)
graphql_location_query = """
{{
    search(categories: "bubbletea",
            location: "{state}, {zip_code}",
            limit: {limit},
            sort_by: "{sort_by}") {{
            business {{
                id
                name
                phone
                rating
                review_count
                alias
                url
                coordinates {{
                    latitude
                    longitude
                }}
                location {{
                    city
                    country
                    address1
                    address2
                    address3
                    state
                    zip_code
                }}
            }}
        }}
}}
"""

# GraphQL business query
# (see https://www.yelp.com/developers/graphql/query/business)
graphql_business_hours_query = """
{{
     business(id: "{id}") {{
        hours {{
            open {{
                is_overnight
                end
                day
                start
            }}
        }}
    }}
}}
"""


class BubbleTeaImport:

    def __init__(self, import_hours=False):
        """
        Args:
            import_hours: If True, import business hours into the
            hours table in the database
        """
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)
        self.import_hours = import_hours

    def import_to_db(self, zip_code=None,
                     limit=50, sort_by='rating'):
        """
        Takes a zip code and looks for bubble tea shops around that zip code.

        Args:
            zip_code: ZIP code to search for bubble tea shops around
            limit: Max number of results returned by GraphQL query
            sort_by: Sort GraphQL query results by this

        Returns: None
        """
        session = self.Session()

        location_query = {
            'query': graphql_location_query.format(
                state=STATE,
                zip_code=zip_code,
                limit=limit,
                sort_by=sort_by
            )
        }

        search_res = requests.post(
            url=api_url,
            headers=headers,
            json=location_query
        )

        try:
            businesses = search_res.json()['data']['search']['business']
            print("Found {} businesses around zip_code={}".format(
                len(businesses), zip_code
            ))
        except:
            print("No businesses found.")
            return

        for business in businesses:
            if business['location']['state'] != STATE:
                continue

            id = business['id']
            alias = business['alias']
            name = business['name']

            location = business['location']
            for k, v in location.items():
                if v == '':
                    location[k] = None
            country = location['country']
            address1 = location['address1']
            address2 = location['address2']
            address3 = location['address3']
            city = location['city']
            state = location['state']
            zip_code = location['zip_code']

            phone = business['phone'] if business['phone'] is not '' else None
            coordinates = business['coordinates']
            longitude = coordinates['longitude']
            latitude = coordinates['latitude']
            rating = business['rating']
            review_count = business['review_count']
            url = business['url']

            bubble_tea_dict = {
                'id': id,
                'alias': alias,
                'name': name,
                'country': country,
                'address1': address1,
                'address2': address2,
                'address3': address3,
                'city': city,
                'state': state,
                'zip_code': zip_code,
                'phone': phone,
                'longitude': longitude,
                'latitude': latitude,
                'rating': rating,
                'review_count': review_count,
                'url': url
            }

            session.merge(BubbleTea(**bubble_tea_dict))

            if self.import_hours:
                hours_query = {
                    'query': graphql_business_hours_query.format(id=id)
                }

                hours_res = requests.post(
                    url=api_url, headers=headers, json=hours_query
                )

                try:
                    hours = hours_res\
                        .json()['data']['business']['hours'][0]['open']
                except:
                    continue

                for hour in hours:
                    hour_dict = {
                        'bubble_tea_id': id,
                        'day': hour['day'],
                        'start': hour['start'],
                        'end': hour['end'],
                        'is_overnight': hour['is_overnight']
                    }

                    upsert_stmt = """
                    INSERT INTO hours (
                        bubble_tea_id,
                        day,
                        start,
                        "end",
                        is_overnight
                    )
                    VALUES (
                        '{bubble_tea_id}',
                        {day},
                        '{start}',
                        '{end}',
                        {is_overnight}
                    )
                    ON CONFLICT (bubble_tea_id, day)
                    DO UPDATE SET
                        start = '{start}',
                        "end" = '{end}',
                        is_overnight = {is_overnight}
                    ;
                    """.format(**hour_dict)
                    session.execute(upsert_stmt)
            session.commit()
        session.close()

    def get_locations(self):
        """
        Gets zip codes for the state defined
        by the STATE variable set in settings.py
        """
        session = self.Session()
        locations = session.query(
            ZipCode.zip
        ).filter(
            ZipCode.state == STATE,
        )
        session.close()
        return (loc for loc in locations)


def main():
    bubble_tea = BubbleTeaImport(IMPORT_HOURS)
    for location in bubble_tea.get_locations():
        zip_code = location.zip
        print(
            "Working on importing bubbletea "
            "locations around zip_code = {}".format(zip_code)
        )
        bubble_tea.import_to_db(zip_code=zip_code)


if __name__ == '__main__':
    main()
