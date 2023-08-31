from library.libraries import *
from functions.functions import *

st.title("Country, State, and City Selector using Nominatim API")

country_list = ["Canada", "United States"]
selected_country = st.selectbox("Select a country", country_list)

# Get country code from selected country name
country_code = get_country_code(selected_country)

# Get OSM id and OSM type of the selected country using country code
osm_id, osm_type = get_country_osm_id(country_code)

# If OSM id and OSM type exist, then fetch country details
if osm_id and osm_type:
    country_details = get_country_details(osm_id, osm_type)
else:
    country_details = []

if country_details:
    states = [detail['address']['state']
              for detail in country_details if 'address' in detail and 'state' in detail['address']]
    selected_state = st.selectbox("Select a state", states)

    cities = [detail['address']['city']
              for detail in country_details if 'address' in detail and 'city' in detail['address']]
    selected_city = st.selectbox("Select a city", cities)

    st.write(
        f"You selected: {selected_country} -> {selected_state} -> {selected_city}")
else:
    st.write("No details found for the selected country.")
