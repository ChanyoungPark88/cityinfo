from library.libraries import *


BASE_URL = os.environ.get("BASE_URL")


def get_available_countries():
    """Available countries for the app."""
    return [country.name for country in pycountry.countries]


def get_country_info(country_name):
    params = {
        "country": country_name,
        "format": "json"
    }
    headers = {
        "User-Agent": "getlocinfo"  # 앱의 이름을 지정
    }
    response = requests.get(BASE_URL, params=params, headers=headers)
    st.write(response.json())
    return response.json()
