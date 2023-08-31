from library.libraries import *
from functions.functions import *

st.title("Country, State, and City Selector using Nominatim API")

countries = get_available_countries()
selected_country = st.selectbox("Select a country", countries)

if selected_country:
    # 주 선택
    states = get_state_info(selected_country)
    state_names = [state["display_name"].split(",")[0] for state in states]
    selected_state = st.selectbox("Select a state", state_names)

    if selected_state:
        # 도시 선택
        cities = get_city_info(selected_country, selected_state)
        city_names = [city["display_name"].split(",")[0] for city in cities]
        selected_city = st.selectbox("Select a city", city_names)

        if selected_city:
            # 결과 출력
            st.write(
                f"You selected: {selected_country} > {selected_state} > {selected_city}")
