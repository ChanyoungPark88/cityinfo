from library.libraries import *
from functions.functions import *

st.title("Get Location Info")

countries = get_available_countries()
selected_country = st.selectbox("Select Country", countries)
country_info = get_country_info(selected_country)
st.write(f"You selected {country_info}")
