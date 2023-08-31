from library.libraries import *

headers = {
    "User-Agent": "Get Location Info"  # 앱의 이름을 지정
}

SEARCH_URL = os.environ.get("SEARCH_URL")
LOOKUP_URL = os.environ.get("LOOKUP_URL")


def get_osm_id_for_country(country_name, SEARCH_URL):
    params = {
        "q": country_name,
        "format": "json",
        "limit": 1,  # 첫 번째 결과만 반환
        "countrycodes": country_name
    }
    response = requests.get(SEARCH_URL, params=params, headers=headers)
    if response.status_code == 200 and response.json():
        return response.json()[0]['osm_id']
    else:
        return None


def get_detailed_info_by_osm_id(osm_id, LOOKUP_URL):
    params = {
        "osm_ids": f"R{osm_id}",  # R은 관계(Relation)를 의미
        "format": "json"
    }
    response = requests.get(LOOKUP_URL, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # 데이터를 적절하게 파싱하여 필요한 정보를 추출합니다.
        states = [info['address']['state']
                  for info in data if 'state' in info['address']]
        cities = [info['address']['city']
                  for info in data if 'city' in info['address']]
        return {
            'states': states,
            'cities': cities
        }
    else:
        return None
