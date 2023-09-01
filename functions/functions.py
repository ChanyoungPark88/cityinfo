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
    return pycountry.countries.get(name=country_name).alpha_2


def get_state_code(country_name, state_name):
    try:
        subdivisions = list(pycountry.subdivisions.get(
            country_name=country_name))
        for subdivision in subdivisions:
            if subdivision.name == state_name:
                return subdivision.code.split('-')[-1]  # 'US-CA'에서 'CA' 부분만 반환
        return None
    except Exception:
        return None


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


def load_all_data():
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
