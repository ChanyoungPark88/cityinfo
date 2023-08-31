import streamlit as st
import requests
import os

GEONAMES_API_ENDPOINT = os.environ.get(GEONAMES_API_ENDPOINT)
GEONAMES_USERNAME = os.environ.get(GEONAMES_USERNAME)


def get_countries():
    url = f"{GEONAMES_API_ENDPOINT}countryInfoJSON?username={GEONAMES_USERNAME}"
    response = requests.get(url)
    countries = response.json().get("geonames", [])
    return {country["countryName"]: country["countryCode"] for country in countries}


def get_states(country_code):
    url = f"{GEONAMES_API_ENDPOINT}admin1CodeJSON?country={country_code}&username={GEONAMES_USERNAME}"
    response = requests.get(url)
    states = response.json().get("geonames", [])
    return {state["name"]: state["adminCode1"] for state in states}


def get_cities(country_code, state_code):
    url = f"{GEONAMES_API_ENDPOINT}searchJSON?country={country_code}&adminCode1={state_code}&featureClass=P&username={GEONAMES_USERNAME}"
    response = requests.get(url)
    cities = response.json().get("geonames", [])
    return [city["name"] for city in cities]


st.title("Country, State, and City Selector")

# 국가 선택
countries = get_countries()
selected_country = st.selectbox("Select a country", list(countries.keys()))

# 주 선택
states = get_states(countries[selected_country])
selected_state = st.selectbox("Select a state", list(states.keys()))

# 도시 선택
cities = get_cities(countries[selected_country], states[selected_state])
selected_city = st.selectbox("Select a city", cities)

# 결과 출력
st.write(
    f"You selected: {selected_country} > {selected_state} > {selected_city}")
