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
    return data_frame["state_name"].unique().tolist()


def get_provinces_from_canada(data_frame):
    """
    Retrieve unique provinces from the provided DataFrame.

    Parameters:
    - data_frame (DataFrame): DataFrame containing the data of cities in Canada.

    Returns:
    List: A list of unique provinces.
    """
    return data_frame["province_name"].unique().tolist()


def get_cities_from_state(data_frame, state_name):
    """
    Retrieve cities for the specified state.

    Parameters:
    - df (DataFrame): DataFrame containing the data of cities in the USA.
    - state_name (str): Name of the state to retrieve cities for.

    Returns:
    List: A list of cities for the specified state.
    """
    return data_frame[data_frame["state_name"] == state_name]["city"].tolist()


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


def generate_zillow_url(city, state_or_province, lat, lng):
    """_summary_

    Args:
        city (_type_): _description_
        state_or_province (_type_): _description_
        lat (_type_): _description_
        lng (_type_): _description_

    Returns:
        _type_: _description_
    """
    base_url = "https://www.zillow.com"

    # 대략적인 지도의 경계값을 계산합니다 (예: +/-0.5도)
    north = lat + 0.5
    south = lat - 0.5
    east = lng + 0.5
    west = lng - 0.5

    # URL을 생성합니다
    url = (
        f"{base_url}/{city}-{state_or_province}/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C"
        f"%22mapBounds%22%3A%7B%22north%22%3A{north}%2C%22east%22%3A{east}%2C%22south%22%3A{south}%2C%22west%22%3A{west}%7D%2C"
        "%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D"
    )
    return url
