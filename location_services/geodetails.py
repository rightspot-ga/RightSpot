# HTTP Request: GET {{baseURL}}/api/location_services/geodetails
# Query Parameters: lat (float), lng (float)

import requests
import xmltodict
import json
from main_app.static_data.lookups import districts

def geoDetails(lat, lon):
    # Get details about a location using nominatim.org Reverse API.
    # Input must be a latitude and longitude, formatted as floats.
    # Example: (51.508368, -0.274432)
    # Returns a dictionary of location details, including the district.

    # Build the URL for the Nominatim API request
    url = 'https://nominatim.openstreetmap.org/reverse'
    params = {
        'lat':lat,
        'lon':lon
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = xmltodict.parse(response.content)
        addressparts = data['reversegeocode']['addressparts']
        data_processed = addressparts
        data_processed['district'] = check_uk_district(addressparts)
    
    # If the district is not in the addressparts, use mapit to get the district
    if data_processed['district'] is None:
        mapit_data = mapit(lat, lon)
        # Add mapit data to data_processed
        for key, value in mapit_data.items():
            data_processed[key] = value
            for district in districts:
                if district in value:
                    data_processed['district'] = district
                    break

    if response.status_code == 200:
        return data_processed

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

def mapit(lat, lon):
    # Get details about a location using mapit.mysociety.org API.    
    url = 'https://mapit.mysociety.org/point/4326/' + str(lon) + ',' + str(lat)
    response = requests.get(url)
    response_dict = json.loads(response.content)

    data_processed = {}

    # Get all types and names from the response
    for child in response_dict.values():
        if isinstance(child, dict) and 'type' in child and 'name' in child:
            data_processed[child['type']] = child['name']
            
    return data_processed
