from library.libraries import *
from functions.functions import *


st.title("Country, State, and City Selector using Nominatim API")

# 국가 선택
countries = ["United States", "Canada"]  # 예시로 두 개의 국가만 사용
selected_country = st.selectbox("Select a country", countries)
osm_id_country = get_osm_id_for_country(selected_country, SEARCH_URL)

# 주 선택
if osm_id_country:
    state_info = get_detailed_info_by_osm_id(osm_id_country, LOOKUP_URL)
    if state_info:
        states = [info['display_name']
                  for info in state_info if info['type'] == 'state']
        selected_state = st.selectbox("Select a state", states)

        # 도시 선택
        cities = [info['display_name'] for info in state_info if info['type']
                  == 'city' and selected_state in info['display_name']]
        if cities:
            st.selectbox("Select a city", cities)
