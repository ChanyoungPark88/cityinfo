"""
This module imports necessary libraries for a Streamlit application.
It provides all the required external libraries and functions needed for the app's functionality
such as Google Cloud Storage access, data manipulation with pandas,
and user interface with Streamlit.
"""
from library.libraries import (
    base64, json, os, storage, URLError, st, pd, io
)


BUCKET_NAME = os.environ.get('BUCKET_NAME')


def gcs_connect():
    """
    Connect to Google Cloud Storage using the provided environment variable.

    Returns:
    storage_client(storage.Client): A Google Cloud Storage client object or None if an error occurs.
    """
    # KEY Loading & Decoding
    key_content_encoded = os.environ.get('GOOGLE_CLOUD_KEY_CONTENTS')
    if not key_content_encoded:
        st.write("Key content is missing from environment variables.")
        return None

    key_content = base64.b64decode(key_content_encoded).decode()
    key_data = json.loads(key_content)

    try:
        storage_client = storage.Client.from_service_account_info(key_data)
        return storage_client

    except URLError as error_message:
        st.write(error_message)
        return None


def download_file_from_gcs(filename, storage_client, bucket_name=BUCKET_NAME):
    """
    Download a file from a Google Cloud Storage bucket.

    Parameters:
    - filename (str): The name of the file to download.
    - storage_client (storage.Client): The Google Cloud Storage client.
    - prefix (str): The folder prefix in the bucket.
    - bucket_name (str, optional): The name of the bucket. Defaults to BUCKET_NAME.

    Returns:
    DataFrame or None: A DataFrame containing the downloaded data or None if the file doesn't exist.
    """
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(filename)

    if not blob.exists():
        return None

    content = blob.download_as_text()
    data_frame = pd.read_csv(io.StringIO(content))
    return data_frame


def get_states_from_usa(data_frame):
    """
    Retrieve unique states from the provided DataFrame.

    Parameters:
    - data_frame (DataFrame): DataFrame containing the data of cities in the USA.

    Returns:
    List: A list of unique states.
    """
    sorted_df = data_frame.sort_values(by="SizeRank")

    return sorted_df["state_name"].dropna().astype(str).unique().tolist()


def get_cities_from_state(data_frame, state_name):
    """
    Retrieve cities for the specified state.

    Parameters:
    - data_frame (DataFrame): DataFrame containing the data of cities in the USA.
    - state_name (str): Name of the state to retrieve cities for.

    Returns:
    List: A list of cities for the specified state.
    """
    if not state_name or state_name not in data_frame["state_name"].tolist():
        # 선택한 주가 없거나 데이터프레임에 존재하지 않을 경우 빈 리스트를 반환합니다.
        return []

    # 'SizeRank' 기준으로 데이터프레임을 오름차순으로 정렬합니다.
    sorted_df = data_frame.sort_values(by="SizeRank")

    # 선택한 주(State)에 해당하는 도시들을 필터링하고, NaN 값을 제거한 후 문자열 리스트로 반환합니다.
    return sorted_df[sorted_df["state_name"] == state_name]["city"].dropna().astype(str).tolist()


def get_region_id_from_csv(data_frame, city, state_or_province):
    """
    Retrieve RegionID for the specified city and state from a DataFrame.

    Args:
    - data_frame (DataFrame): DataFrame containing city data.
    - city (str): Name of the city.
    - state_or_province (str): Name of the state or province.

    Returns:
    - int: RegionID of the city. None if not found.
    """
    # Matching city and state name to get RegionID
    matching_row = data_frame[
        (data_frame["city"] == city) & (
            data_frame["state_name"] == state_or_province)
    ]

    if not matching_row.empty:
        return int(matching_row["RegionID"].iloc[0])
    return None


def generate_zillow_url(city, state_or_province, lat, lng, region_id, region_type):
    base_url = "https://www.zillow.com"
    city = city.replace(" ", "-")

    north = lat + 0.5
    south = lat - 0.5
    east = lng + 0.5
    west = lng - 0.5

    if region_type == "city":
        region_type_value = 6
    else:
        region_type_value = 6

    url_path = f"{base_url}/{city.lower()}-{state_or_province.lower()}/houses/"
    query_pagination = "%7B%22pagination%22%3A%7B%7D%2C"
    query_user_term = f"%22userssearchterm%22%3A%22{city}%2C%20{state_or_province}%22%2C"
    query_map_bounds = (f"%22mapbounds%22%3A%7B%22west%22%3A{west}%2C%22east%22%3A{east}%2C"
                        f"%22south%22%3A{south}%2C%22north%22%3A{north}%7D%2C")
    query_region = (f"%22regionselection%22%3A%5B%7B%22regionid%22%3A{region_id}%2C"
                    f"%22regiontype%22%3A{region_type_value}%7D%5D%2C")
    query_map_vis = "%22ismapvisible%22%3Atrue%2C"
    query_filter_state = ("%22filterstate%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C"
                          "%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mapzoom%22%3A11%7D%2C")
    query_list_vis = "%22islistvisible%22%3Atrue%7D"

    url = " ".join([
        f"{url_path}?searchquerystate=",
        f"{query_pagination}",
        f"{query_user_term}",
        f"{query_map_bounds}",
        f"{query_region}",
        f"{query_map_vis}",
        f"{query_filter_state}",
        f"{query_list_vis}"
    ])

    return url


def get_provinces_from_canada(data_frame):
    """
    Retrieve unique provinces from the provided DataFrame.

    Parameters:
    - data_frame (DataFrame): DataFrame containing the data of cities in Canada.

    Returns:
    List: A list of unique provinces.
    """
    return data_frame["province_name"].unique().tolist()


def get_cities_from_province(data_frame, province_name):
    """
    Retrieve cities for the specified province.

    Parameters:
    - df (DataFrame): DataFrame containing the data of cities in Canada.
    - province_name (str): Name of the province to retrieve cities for.

    Returns:
    List: A list of cities for the specified province.
    """
    return data_frame[data_frame["province_name"] == province_name]["city"].tolist()
