from library.libraries import *
from functions.functions import *

st.title("Country, State, and City Selector using Nominatim API")

# Dummy list for demonstration. This should be replaced by a real country list.
country_list = ["USA", "Germany", "France", "South Korea"]
selected_country = st.selectbox("Select a country", country_list)

country_details = get_state_and_city_details(selected_country)
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
