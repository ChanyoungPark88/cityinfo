from library.libraries import *
from functions.functions import *

st.title("Country, State, and City Selector using Nominatim API")

selected_country = st.selectbox("Select a country")

# 선택한 나라의 정보를 가져옵니다.
country_info = get_country_info(selected_country)
st.write(f"Selected Country: {selected_country}")
st.write(country_info)
