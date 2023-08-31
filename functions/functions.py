from library.libraries import *

SEARCH_URL = "https://nominatim.openstreetmap.org/search"
LOOKUP_URL = "https://nominatim.openstreetmap.org/lookup"


def get_country_code(country_name):
    return pycountry.countries.get(name=country_name).alpha_2


def get_country_osm_id(country_code):
    params = {
        "q": country_code,
        "format": "json",
        "limit": 1,
        "addressdetails": 1
    }
    response = requests.get(SEARCH_URL, params=params).json()
    if response and 'country_code' in response[0]['address'] and response[0]['address']['country_code'].lower() == country_code.lower():
        return response[0]['osm_id'], response[0]['osm_type']
    else:
        return None, None


def get_country_details(osm_id, osm_type):
    params = {
        "osm_ids": f"{osm_type[0]}{osm_id}",
        "format": "jsonv2"
    }
    return requests.get(LOOKUP_URL, params=params).json()


def get_state_and_city_details(osm_id, osm_type):
    details = get_country_details(osm_id, osm_type)
    if osm_id and osm_type:
        details = get_country_details(osm_id, osm_type)
        return details
    else:
        return []
