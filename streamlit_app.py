from library.libraries import *
from functions.functions import *

st.title("Country, State, and City Selector using Geonames API")

# pycountry를 통해 국가 리스트를 가져옵니다.
country_list = ["Canada", "United States"]  # 현재 예시에서는 두 국가만 사용합니다.
selected_country_name = st.selectbox("Select a country", country_list)

if selected_country_name:
    # 선택된 국가의 이름을 국가 코드로 변환합니다.
    selected_country_code = get_country_code(selected_country_name)

    # 국가 코드를 사용하여 해당 국가의 주/지방 목록을 가져옵니다.
    state_data = get_states(selected_country_code)
    state_names = [state["name"] for state in state_data]
    selected_state_name = st.selectbox("Select a state", state_names)

    if selected_state_name:
        # 선택된 주/지방의 이름을 주/지방 코드로 변환합니다.
        selected_state_code = next(
            state["code"] for state in state_data if state["name"] == selected_state_name)

        # 주/지방 코드를 사용하여 해당 주/지방의 도시 목록을 가져옵니다.
        city_data = get_cities(selected_state_code)
        city_names = [city["name"] for city in city_data]
        selected_city_name = st.selectbox("Select a city", city_names)

        if selected_city_name:
            st.write(
                f"You selected: {selected_country_name} -> {selected_state_name} -> {selected_city_name}")
