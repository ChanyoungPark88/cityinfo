from library.libraries import *
from functions.functions import *

st.title("Country, State, and City Selector using Restcountries API")

# pycountry를 통해 국가 리스트를 가져옵니다.
country_list = ["Canada", "United States"]  # 현재 예시에서는 두 국가만 사용합니다.
selected_country_name = st.selectbox("Select a country", country_list)

# 선택된 국가의 이름을 국가 코드로 변환합니다.
selected_country_code = get_country_code(selected_country_name)

# 국가 코드를 사용하여 해당 국가의 상세 정보를 가져옵니다.
state_data = get_states(selected_country_code)

city_data = get_cities(state_data)

st.write(
    f"You selected: {selected_country_name} -> {state_data} -> {city_data}")
