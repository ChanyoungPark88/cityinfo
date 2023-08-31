from library.libraries import *


BASE_URL = os.environ.get("BASE_URL")


def get_available_countries():
    """Available countries for the app."""
    return [country.name for country in pycountry.countries if country.name in ["Canada", "United States"]]


def get_country_info(country_name):
    if country_name not in ["Canada", "USA"]:
        return []

    params = {
        "country": country_name,
        "format": "json"
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()


def get_state_info(country_name):
    params = {
        "country": country_name,
        "polygon_geojson": 1,
        "format": "json"
    }
    response = requests.get(BASE_URL, params=params)
    states = [place for place in response.json() if place['type'] == 'state']
    return states


def get_city_info(country_name, state_name):
    params = {
        "country": country_name,
        "state": state_name,
        "format": "json"
    }
    response = requests.get(BASE_URL, params=params)
    cities = [place for place in response.json() if place['type'] == 'city']
    return cities
