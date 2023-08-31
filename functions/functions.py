from library.libraries import *

SEARCH_URL = "https://nominatim.openstreetmap.org/search"
LOOKUP_URL = "https://nominatim.openstreetmap.org/lookup"


def get_country_osm_id(country_name):
    params = {
        "q": country_name,
        "format": "json",
        "limit": 1,
        "addressdetails": 1
    }
    response = requests.get(SEARCH_URL, params=params).json()
    if response:
        return response[0]['osm_id'], response[0]['osm_type']
    else:
        return None, None


def get_country_details(osm_id, osm_type):
    params = {
        "osm_ids": f"{osm_type[0]}{osm_id}",
        "format": "json"
    }
    return requests.get(LOOKUP_URL, params=params).json()


def get_state_and_city_details(country_name):
    osm_id, osm_type = get_country_osm_id(country_name)
    if osm_id and osm_type:
        details = get_country_details(osm_id, osm_type)
        return details
    else:
        return []
