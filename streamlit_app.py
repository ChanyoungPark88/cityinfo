"""_summary_: This is a Streamlit app that generates a Zillow search URL
based on the user's country, state, and city selections.
"""
from library.libraries import st
from function.functions import gcs_connect, download_file_from_gcs

st.title("Zillow Search URL Generator using Country, State, and City")

# pycountry를 통해 국가 리스트를 가져옵니다.
country_list = ["Canada", "United States"]  # 현재 예시에서는 두 국가만 사용합니다.
selected_country_name = st.selectbox(
    "Select a country", ["Select a country"] + country_list)

if selected_country_name == "Canada":
    FILENAME = "canadacities_selected.csv"
elif selected_country_name == "United States":
    FILENAME = "uscities_selected.csv"
else:
    FILENAME = None

if FILENAME:
    storage_client = gcs_connect()
    if storage_client:  # Ensure that the storage client was successfully initialized
        data_frame = download_file_from_gcs(FILENAME, storage_client)
        if data_frame is not None:
            # Display the data or do further processing...
            st.write(data_frame)
