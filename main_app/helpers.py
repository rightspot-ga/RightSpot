import requests

def fetch_from_api(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def get_api_base_url(request):
    return request.scheme + '://' + request.get_host() + '/api'