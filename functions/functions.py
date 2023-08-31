from library.libraries import *

GEONAMES_URL = os.environ.get("GEONAMES_URL")
GEONAMES_USERNAME = os.environ.get("GEONAMES_USERNAME")
COUNTRY_INFO_URL = os.environ.get("COUNTRY_INFO_URL")


def get_all_country_geoname_ids():
    response = requests.get(COUNTRY_INFO_URL, params={
                            "username": GEONAMES_USERNAME})
    data = response.json()

    country_geoname_ids = {}
    for country in data['geonames']:
        country_code = country['countryCode']
        geoname_id = country['geonameId']
        country_geoname_ids[country_code] = geoname_id

    return country_geoname_ids


def get_country_code(country_name):
    if country_name == "Please select a country":
        return None
    return pycountry.countries.get(name=country_name).alpha_2


def get_states(country_code):
    country_geoname_ids = get_all_country_geoname_ids()
    country_geoname_id = country_geoname_ids.get(country_code)

    response = requests.get(GEONAMES_URL, params={
        "geonameId": country_geoname_id,
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
