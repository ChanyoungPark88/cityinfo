from library.libraries import *
from functions.functions import *

country_names = [country.name for country in pycountry.countries]

selected_country = st.selectbox("Select a country", country_names)
st.write(f"You selected: {selected_country}")
