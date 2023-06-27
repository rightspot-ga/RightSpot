import requests

def fetch_from_api(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def get_api_base_url(request):
    return request.scheme + '://' + request.get_host() + '/api'

def format_value_as_integer_or_dash(value):
    try:
        float_value = float(value)
        if float_value == 0:
            return '-'
        elif float_value.is_integer():
            return int(float_value)
        else:
            return float_value
    except ValueError:
        return value