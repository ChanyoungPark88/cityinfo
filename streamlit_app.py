from library.libraries import *
from functions.functions import *

st.title("Zillow Search URL Generator using Country, State, and City")

# 초기 시작 시 모든 데이터를 로딩
all_countries = get_all_countries()
all_states = get_all_states()
all_cities = get_all_cities()

# 국가 선택 Dropdown
selected_country_name = st.selectbox(
    "Select a country", ["Select a country"] + list(all_countries.keys()))

# 선택된 국가에 따른 주/지방 목록 필터링 및 Dropdown
if selected_country_name and selected_country_name != "Select a country":
    states_in_selected_country = all_states[selected_country_name]
    selected_state_name = st.selectbox(
        "Select a state", ["Select a state"] + states_in_selected_country)

    # 선택된 주/지방에 따른 도시 목록 필터링 및 Dropdown
    if selected_state_name and selected_state_name != "Select a state":
        cities_in_selected_state = all_cities[selected_state_name]
        selected_city_name = st.selectbox(
            "Select a city", ["Select a city"] + cities_in_selected_state)

        if selected_city_name and selected_city_name != "Select a city":
            city_name_for_url = selected_city_name.lower().replace(" ", "-")
            state_code_for_url = get_state_code(
                selected_country_name, selected_state_name)
            zillow_url = f"https://www.zillow.com/{city_name_for_url}-{state_code_for_url.lower()}/"
            st.write(f"Zillow Search URL: {zillow_url}")
