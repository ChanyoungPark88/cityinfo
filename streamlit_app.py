from library.libraries import *
from functions.functions import *

st.title("Country, State, and City Selector using Restcountries API")

# pycountry를 통해 국가 리스트를 가져옵니다.
country_list = ["Canada", "United States"]  # 현재 예시에서는 두 국가만 사용합니다.
selected_country_name = st.selectbox("Select a country", country_list)

# 선택된 국가의 이름을 국가 코드로 변환합니다.
selected_country_code = get_country_code(selected_country_name)

# 국가 코드를 사용하여 해당 국가의 상세 정보를 가져옵니다.
country_data = get_country(selected_country_code)

# 국가 데이터를 사용하여 주와 도시의 정보를 가져옵니다.
# 주의: 현재 get_state와 get_city 함수에서는 간단한 예시 값만 반환합니다.
# 실제 데이터를 반환하려면 다른 API 또는 데이터 소스가 필요합니다.
state_data = get_state(country_data)
city_data = get_city(state_data)

st.write(
    f"You selected: {selected_country_name} -> {state_data} -> {city_data}")
