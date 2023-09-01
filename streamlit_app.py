from library.libraries import *
from functions.functions import *

# 전역 변수로 모든 데이터 로드
ALL_COUNTRY_IDS, ALL_STATES, ALL_CITIES = load_all_data()

st.title("Zillow Search URL Generator using Country, State, and City")

country_list = list(ALL_COUNTRY_IDS.keys())
selected_country_name = st.selectbox(
    "Select a country", ["Select a country"] + country_list)

if selected_country_name != "Select a country":
    state_data = ALL_STATES.get(selected_country_name)
    state_names = [state["name"] for state in state_data]
    selected_state_name = st.selectbox(
        "Select a state", ["Select a state"] + state_names)

    if selected_state_name:
        city_data = ALL_CITIES.get(selected_state_name)
        city_names = [city["name"] for city in city_data]
        selected_city_name = st.selectbox(
            "Select a city", ["Select a city"] + city_names)

        if selected_city_name:
            city_name_for_url = selected_city_name.lower().replace(" ", "-")
            state_code_for_url = get_state_code(
                selected_country_name, selected_state_name)
            zillow_url = f"https://www.zillow.com/{city_name_for_url}-{state_code_for_url.lower()}/"
            st.write(f"Zillow Search URL: {zillow_url}")
