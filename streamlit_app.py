"""_summary_: This is a Streamlit app that generates a Zillow search URL
based on the user's country, state, and city selections.
"""
from library.libraries import st
from function.functions import (
    gcs_connect, download_file_from_gcs,
    get_states_from_usa,
    get_cities_from_state,
    generate_zillow_url
)

st.title("Zillow Search URL Generator using Country, State, and City")

country_list = ["United States"]
selected_country_name = st.selectbox(
    "Select a country", ["Select a country"] + country_list)

storage_client = gcs_connect()
if not storage_client:
    st.error("Failed to connect to Google Cloud Storage.")

elif selected_country_name == "United States":
    FILENAME = "merged_usacities_data.csv"
    data_frame = download_file_from_gcs(FILENAME, storage_client)
    if data_frame is not None:
        # 주(State) 선택 드롭다운 생성
        states = ["Select a state"] + sorted(get_states_from_usa(data_frame))
        selected_state = st.selectbox("Select a state", states)

        # 선택된 주(State)에 해당하는 도시 선택 드롭다운 생성
        if selected_state != "Select a state":
            cities = ["Select a city"] + \
                sorted(get_cities_from_state(data_frame, selected_state))
            selected_city = st.selectbox("Select a city", cities)

            if selected_city != "Select a city":
                city_data = data_frame[data_frame["city"]
                                       == selected_city].iloc[0]
                city_lat = city_data['lat']
                city_lng = city_data['lng']
                state_id = city_data['state_id']

                zillow_url = generate_zillow_url(
                    selected_city, state_id, city_lat, city_lng)
                st.write(f"Zillow URL: {zillow_url}")
