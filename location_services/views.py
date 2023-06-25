from django.http import JsonResponse
from rest_framework.decorators import api_view
from .geocoding import geocodeGoogle, geocodeWhat3Words
from .geodetails import geoDetails
from .geoplaces import nearbyPlaces
import re
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

regexWhat3Words = r"^/*(?:[^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]{1,}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]{1,}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]{1,}|'<,.>?/\";:£§º©®\s]+[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+|[^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+([\u0020\u00A0][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+){1,3}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+([\u0020\u00A0][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+){1,3}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+([\u0020\u00A0][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+){1,3})$"

@swagger_auto_schema(
    method='get',
    operation_summary='Geocode a location',
    manual_parameters=[
        openapi.Parameter(
            name='query',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='The location to geocode. <br> Can be a place name, postcode, or what3words address.',
            required=True,
        ),
    ],
    responses={
        200: openapi.Response(
            description='Successful geocode',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'lat': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'lng': openapi.Schema(type=openapi.TYPE_NUMBER),
                },
            ),
        ),
        400: openapi.Response(
            description='Invalid input or geocode error',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        ),
    },
)
@api_view(['GET'])
def geocode(request):
    query = request.GET.get('query')

    if query and re.search(regexWhat3Words, query, flags=re.UNICODE):
        try:
            lat, lng = geocodeWhat3Words(query)
            return JsonResponse({'lat': lat, 'lng': lng})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    elif query:
        try:
            lat, lng = geocodeGoogle(query)
            return JsonResponse({'lat': lat, 'lng': lng})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid Input: API/Geocode'}, status=400)
    
@swagger_auto_schema(
    method='get',
    operation_summary='Get location details',
    manual_parameters=[
        openapi.Parameter(
            name='lat',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='The latitude of the location',
            required=True,
        ),
        openapi.Parameter(
            name='lng',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='The longitude of the location',
            required=True,
        ),
    ],
    responses={
        200: openapi.Response(
            description='Successful location details',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'highway': openapi.Schema(type=openapi.TYPE_STRING),
                    'road': openapi.Schema(type=openapi.TYPE_STRING),
                    'suburb': openapi.Schema(type=openapi.TYPE_STRING),
                    'town': openapi.Schema(type=openapi.TYPE_STRING),
                    'city': openapi.Schema(type=openapi.TYPE_STRING),
                    'county': openapi.Schema(type=openapi.TYPE_STRING),
                    'ISO3166-2-lvl6': openapi.Schema(type=openapi.TYPE_STRING),
                    'state': openapi.Schema(type=openapi.TYPE_STRING),
                    'ISO3166-2-lvl4': openapi.Schema(type=openapi.TYPE_STRING),
                    'postcode': openapi.Schema(type=openapi.TYPE_STRING),
                    'country': openapi.Schema(type=openapi.TYPE_STRING),
                    'country_code': openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        ),
        400: openapi.Response(
            description='Invalid input or location details error',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        ),
    },
)
@api_view(['GET'])
def location_details(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lng')

    if lat and lon:
        try:
            details = geoDetails(lat, lon)
            return JsonResponse(details)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid Input: API/Location Details'}, status=400)
    
@swagger_auto_schema(
    method='get',
    operation_summary='Get nearby places',
    manual_parameters=[
        openapi.Parameter(
            name='lat',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='The latitude of the location',
            required=True,
        ),
        openapi.Parameter(
            name='lng',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='The longitude of the location',
            required=True,
        ),
        openapi.Parameter(
            name='radius',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='The radius of the search area in meters',
            required=True,
        ),
    ],
    responses={
        200: openapi.Response(
            description='Successful nearby places',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'results': openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        ),
        400: openapi.Response(
            description='Invalid input or nearby places error',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        ),
    },
)
@api_view(['GET'])   
def location_places(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    radius = request.GET.get('radius')

    if lat and lng and radius:
        try:
            places = nearbyPlaces(lat, lng, radius)
            return JsonResponse(places)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid Input: API/Nearby Places'}, status=400)
    