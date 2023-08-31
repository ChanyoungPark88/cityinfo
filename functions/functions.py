from library.libraries import *


BASE_URL = os.environ.get("BASE_URL")


def get_country_info(country_name):
    params = {
        "country": country_name,
        "format": "json"
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()
