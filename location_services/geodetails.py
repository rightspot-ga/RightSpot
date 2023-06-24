# HTTP Request: GET {{baseURL}}/api/location_services/geodetails
# Query Parameters: lat (float), lng (float)

import requests
import xmltodict
from main_app.static_data.lookups import districts

def geoDetails(lat, lon):
    # Get details about a location using nominatim.org Reverse API.
    # Input must be a latitude and longitude, formatted as floats.
    # Example: (51.508368, -0.274432)

    # Build the URL for the API request
    url = 'https://nominatim.openstreetmap.org/reverse'
    params = {
        'lat':lat,
        'lon':lon
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = xmltodict.parse(response.content)
        return data['reversegeocode']['addressparts']

def check_uk_district(addressparts):
    if addressparts['country'] != 'United Kingdom':
        return None
    for key, value in addressparts.items():
        if value in districts:
            return value
        if value.startswith('London Borough of '):
            borough = value.replace('London Borough of ', '')
            if borough in districts:
                return borough
    return None

