from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .geocoding import geocodeGoogle, geocodeWhat3Words
from .geodetails import geoDetails
from .geoplaces import nearbyPlaces
import re

regexWhat3Words = r"^/*(?:[^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]{1,}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]{1,}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]{1,}|'<,.>?/\";:£§º©®\s]+[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+|[^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+([\u0020\u00A0][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+){1,3}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+([\u0020\u00A0][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+){1,3}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+([\u0020\u00A0][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+){1,3})$"

@require_GET
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
    
@require_GET    
def location_details(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lng')
    print(lat, lon)

    if lat and lon:
        try:
            details = geoDetails(lat, lon)
            return JsonResponse(details)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid Input: API/Location Details'}, status=400)
    
@require_GET
def location_places(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    radius = request.GET.get('radius')

    # print(lat, lng, radius)

    if lat and lng and radius:
        try:
            places = nearbyPlaces(lat, lng, radius)
            return JsonResponse(places)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid Input: API/Nearby Places'}, status=400)
    