from library.libraries import *
from functions.functions import *

st.title("Country, State, and City Selector")

# 국가 선택
countries = get_countries()
selected_country = st.selectbox("Select a country", list(countries.keys()))

# 국가를 선택한 경우 주의 목록 로드
if selected_country in countries:
    states = get_states(countries[selected_country])
else:
    states = {}

selected_state = st.selectbox("Select a state", list(states.keys()))

# 주를 선택한 경우 도시의 목록 로드
if selected_state in states:
    cities = get_cities(countries[selected_country], states[selected_state])
else:
    cities = []

selected_city = st.selectbox("Select a city", cities)

# 결과 출력
if selected_country and selected_state and selected_city:
    st.write(
        f"You selected: {selected_country} > {selected_state} > {selected_city}")
