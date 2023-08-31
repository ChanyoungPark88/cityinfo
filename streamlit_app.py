from library.libraries import *
from functions.functions import *

st.title("Country, State, and City Selector")

# 국가 선택
countries = get_countries()
selected_country = st.selectbox("Select a country", list(countries.keys()))

if selected_country:
    # 주 선택
    states = get_states(countries[selected_country])
    if states:  # 국가에 따라 주 정보가 없을 수 있으므로 확인
        selected_state = st.selectbox("Select a state", list(states.keys()))

        if selected_state:
            # 도시 선택
            cities = get_cities(
                countries[selected_country], states[selected_state])
            if cities:  # 주에 따라 도시 정보가 없을 수 있으므로 확인
                selected_city = st.selectbox("Select a city", cities)

                if selected_city:
                    # 결과 출력
                    st.write(
                        f"You selected: {selected_country} > {selected_state} > {selected_city}")
