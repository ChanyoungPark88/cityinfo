from library.libraries import *


API_ENDPOINT = os.environ.get("GEONAMES_API_ENDPOINT")
USERNAME = os.environ.get("GEONAMES_USERNAME")


def get_countries():
    url = f"{API_ENDPOINT}countryInfoJSON?username={USERNAME}"
    response = requests.get(url)
    countries = response.json().get("geonames", [])
    return {country["countryName"]: country["countryCode"] for country in countries}


# def get_states(country_code):
#     url = f"{API_ENDPOINT}admin1CodeJSON?country={country_code}&username={USERNAME}"
#     response = requests.get(url)
#     states = response.json().get("geonames", [])
#     return {state["name"]: state["adminCode1"] for state in states}
def get_states(country_code):
    url = f"{API_ENDPOINT}admin1CodeJSON?country={country_code}&username={USERNAME}"
    response = requests.get(url)
    st.write(response.text)  # API 응답 출력
    states = response.json().get("geonames", [])
    return {state["name"]: state["adminCode1"] for state in states}


def get_cities(country_code, state_code):
    url = f"{API_ENDPOINT}searchJSON?country={country_code}&adminCode1={state_code}&featureClass=P&username={USERNAME}"
    response = requests.get(url)
    cities = response.json().get("geonames", [])
    return [city["name"] for city in cities]
