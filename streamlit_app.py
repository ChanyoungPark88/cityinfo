from library.libraries import *
from functions.functions import *

# Filter the countries you want to display
country_names = [country.name for country in pycountry.countries if country.name in [
    "Canada", "United States"]]

selected_country = st.selectbox("Select a country", country_names)
st.write(f"You selected: {selected_country}")
