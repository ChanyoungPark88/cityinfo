from library.libraries import *

GEONAMES_URL = "GEONAMES_URL"
GEONAMES_USERNAME = "GEONAMES_USERNAME"


def get_country_code(country_name):
    return pycountry.countries.get(name=country_name).alpha_2


def get_states(country_code):
    response = requests.get(GEONAMES_URL, params={
        "geonameId": get_geoname_id_from_country_code(country_code),
        "username": GEONAMES_USERNAME
    })

    data = response.json()
    return [{"name": state["name"], "code": state["geonameId"]} for state in data["geonames"]]


def get_cities(state_code):
    response = requests.get(GEONAMES_URL, params={
        "geonameId": state_code,
        "username": GEONAMES_USERNAME
    })

    data = response.json()
    return [{"name": city["name"], "code": city["geonameId"]} for city in data["geonames"]]
