"""Streamlit app to generate a Zillow search URL.

Attributes:
    GEONAMES_URL (str): URL for the GeoNames API endpoint.
    GEONAMES_USERNAME (str): Username for the GeoNames API.
    COUNTRY_INFO_URL (str): URL for the country information API endpoint.
"""
from library.libraries import os, requests, pycountry

GEONAMES_URL = os.environ.get("GEONAMES_URL")
GEONAMES_USERNAME = os.environ.get("GEONAMES_USERNAME")
COUNTRY_INFO_URL = os.environ.get("COUNTRY_INFO_URL")


def get_all_country_geoname_ids():
    """Retrieve a dictionary mapping country codes to geoname IDs.

    Returns:
        dict: Dictionary of country codes and corresponding geoname IDs.
    """
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
    """Retrieve the country code based on the country name.

    Args:
        country_name (str): Name of the country.

    Returns:
        str or None: Country code if found, None otherwise.
    """
    try:
        country = pycountry.countries.get(name=country_name)
        return country.alpha_2  # Returns the two-letter country code, e.g., "US"
    except AttributeError:
        return None


def get_state_code(country_name, state_name):
    """Retrieve the state code based on the country and state names.

    Args:
        country_name (str): Name of the country.
        state_name (str): Name of the state.

    Returns:
        str or None: State code if found, None otherwise.
    """
    try:
        # First, get the country code using the country name.
        country_code = get_country_code(country_name)

        subdivisions = list(pycountry.subdivisions.get(
            country_code=country_code))
        for subdivision in subdivisions:
            if subdivision.name == state_name:
                return subdivision.code.split('-')[-1]  # 'US-CA'에서 'CA' 부분만 반환
        return None
    except (AttributeError, KeyError):
        return None


def get_states(country_code):
    """Fetch a list of states for a given country code.

    Args:
        country_code (str): Country code to fetch states for.

    Returns:
        list: List of dictionaries containing state names and geoname IDs.
    """
    country_geoname_ids = get_all_country_geoname_ids()
    country_geoname_id = country_geoname_ids.get(country_code)

    response = requests.get(GEONAMES_URL, params={
        "geonameId": country_geoname_id,
        "username": GEONAMES_USERNAME
    })

    data = response.json()
    return [{"name": state["name"], "code": state["geonameId"]} for state in data["geonames"]]


def get_cities(state_code):
    """Obtain a list of cities for a specified state code.

    Args:
        state_code (str): State code to retrieve cities for.

    Returns:
        list: List of dictionaries containing city names and geoname IDs.
    """
    response = requests.get(GEONAMES_URL, params={
        "geonameId": state_code,
        "username": GEONAMES_USERNAME
    })

    data = response.json()
    print(data)
    return [{"name": city["name"], "code": city["geonameId"]} for city in data["geonames"]]


def load_all_data():
    """Gather a comprehensive set of location data.

    Returns:
        tuple: Tuple containing dictionaries of country codes to geoname IDs,
        states to cities, and states to geoname IDs.
    """
    # 국가 코드와 ID 매핑
    country_ids = get_all_country_geoname_ids()

    # 캐나다와 미국만 필터링
    filtered_country_ids = {code: id for code, id in country_ids.items() if code in [
        'CA', 'US']}

    # 각 국가별 주/지방 정보
    all_states = {country_code: get_states(
        country_code) for country_code in filtered_country_ids.keys()}

    # 각 주/지방별 도시 정보
    all_cities = {state['code']: get_cities(
        state['code']) for states in all_states.values() for state in states}

    return filtered_country_ids, all_states, all_cities
