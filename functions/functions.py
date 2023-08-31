from library.libraries import *

RESTCOUNTRIES_URL = "RESTCOUNTRIES_URL"


def get_country_code(country_name):
    return pycountry.countries.get(name=country_name).alpha_2


def get_country(country_code):
    response = requests.get(f"{RESTCOUNTRIES_URL}/alpha/{country_code}")
    data = response.json()
    return data


def get_state(country_data):
    # Restcountries API에서는 '주'에 해당하는 구체적인 정보를 제공하지 않기 때문에
    # 여기서는 대신 국가 이름을 반환하거나 다른 소스를 사용해야 합니다.
    return country_data['name']['common']


def get_city(state_data):
    # 마찬가지로 '도시'에 해당하는 정보도 제공하지 않으므로
    # 국가 또는 주의 주요 도시를 반환하거나 다른 소스를 사용해야 합니다.
    return "Sample City"
