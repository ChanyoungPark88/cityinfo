"""_summary_: This is a Streamlit app that generates a Zillow search URL
based on the user's country, state, and city selections.
"""
from library.libraries import st
from function.functions import (
    gcs_connect, download_file_from_gcs,
    get_provinces_from_canada, get_states_from_usa,
    get_cities_from_province, get_cities_from_state
)

st.title("Zillow Search URL Generator using Country, State, and City")

country_list = ["Canada", "United States"]
selected_country_name = st.selectbox(
    "Select a country", ["Select a country"] + country_list)

storage_client = gcs_connect()
if not storage_client:
    st.error("Failed to connect to Google Cloud Storage.")

elif selected_country_name == "Canada":
    FILENAME = "canadacities_selected.csv"
    data_frame = download_file_from_gcs(FILENAME, storage_client)
    if data_frame is not None:
        # 주 선택 드롭다운 생성
        provinces = ["Select a province"] + \
            sorted(get_provinces_from_canada(data_frame), reverse=True)
        selected_province = st.selectbox("Select a province", provinces)

        # 선택된 주에 해당하는 도시 선택 드롭다운 생성
        if selected_province != "Select a province":
            cities = ["Select a city"] + \
                sorted(get_cities_from_province(
                    data_frame, selected_province), reverse=True)
            selected_city = st.selectbox("Select a city", cities)

            if selected_city != "Select a city":
                province_id = data_frame[data_frame["province_name"]
                                         == selected_province].iloc[0]['province_id']
                st.write(f"{selected_city}-{province_id}")

elif selected_country_name == "United States":
    FILENAME = "uscities_selected.csv"
    data_frame = download_file_from_gcs(FILENAME, storage_client)
    if data_frame is not None:
        # 주(State) 선택 드롭다운 생성
        states = ["Select a state"] + \
            sorted(get_states_from_usa(data_frame), reverse=True)
        selected_state = st.selectbox("Select a state", states)

        # 선택된 주(State)에 해당하는 도시 선택 드롭다운 생성
        if selected_state != "Select a state":
            cities = ["Select a city"] + \
                sorted(get_cities_from_state(
                    data_frame, selected_state), reverse=True)
            selected_city = st.selectbox("Select a city", cities)

            if selected_city != "Select a city":
                state_id = data_frame[data_frame["state_name"]
                                      == selected_state].iloc[0]['state_id']
                st.write(f"{selected_city}-{state_id}")
