# HTTP Request: GET {{baseURL}}/api/location_services/geodetails
# Query Parameters: lat (float), lng (float)

import requests
import xmltodict

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
