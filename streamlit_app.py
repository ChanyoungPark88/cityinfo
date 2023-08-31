from library.libraries import *
from functions.functions import *

# pycountry 라이브러리를 이용해 국가 리스트를 가져온다.
countries = [country.name for country in pycountry.countries]

# 선택 가능한 국가 리스트
available_countries = ["Canada", "United States"]

st.title("Country, State, and City Selector using Nominatim API")

# 국가 선택 드롭다운
selected_country = st.selectbox("Select a country", available_countries)

# 선택한 국가의 OSM id와 OSM type 가져오기
osm_id, osm_type = get_country_osm_id(selected_country)

# OSM id와 OSM type이 존재하면 국가 정보 가져오기
if osm_id and osm_type:
    country_details = get_country_details(osm_id, osm_type)
    st.write(f"Details for {selected_country}:")
    st.write(country_details)
else:
    st.write("No details found for the selected country.")
