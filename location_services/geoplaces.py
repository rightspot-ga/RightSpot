# HTTP Request: GET {{baseURL}}/api/location_services/nearbyplaces
# Query Parameters: lat (float), lng (float), radius (int)

import environ, os
import requests

environ.Env()
environ.Env.read_env()

def nearbyPlaces(lat, lng, radius):
    # Find nearby places using the Google Maps API.
    # Input must be a latitude and longitude, formatted as floats.
    # Input must also be a radius, formatted as an integer.
    # Example: (51.508368, -0.274432)

    # print(f'{lat},{lng}')

    # Build the URL for the API request
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': f'{lat},{lng}',
        'radius': radius,
        'key': os.environ['GOOGLE_MAPS_API_KEY']
    }

    payload = {}
    headers= {}

    response = requests.get(url, params=params, headers=headers, data = payload)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return {'results': data['results']}
        else:
            return None