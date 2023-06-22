# HTTP Request: GET {{baseURL}}/api/location_services/geocode
# Query Parameters: query (string)
# where query is a 3 word address (format:"<string>.<string>.<string>") or any address (format: "<string> <string> ...")

import environ, os
import requests

environ.Env()
environ.Env.read_env()

def geocodeGoogle(address):
    # Geocode an address using the Google Maps API.
    # Input can be any address.
    # Example: '1600 Amphitheatre Parkway, Mountain View, CA'
    # Example: 'Trafalgar Square, London'

    # Build the URL for the API request
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': address,
        'key': os.environ['GOOGLE_MAPS_API_KEY']
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            result = data['results'][0]
            return (result['geometry']['location']['lat'], result['geometry']['location']['lng'])
        
def geocodeWhat3Words(address):
    # Geocode an address using the What3Words API.
    # Input must be a 3 word address, formatted as a string with dots as separators.
    # Example: 'mile.crazy.shade'

    # Build the URL for the API request
    url = 'https://api.what3words.com/v3/convert-to-coordinates'
    params = {
        'words': address,
        'key': os.environ['WHAT_3_WORDS_API_KEY']
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['coordinates']:
            result = data['coordinates']
            return (result['lat'], result['lng'])