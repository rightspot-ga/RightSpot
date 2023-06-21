from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .geocoding import geocodeGoogle, geocodeWhat3Words
import re

regexWhat3Words = r"^/*(?:[^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]{1,}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]{1,}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]{1,}|'<,.>?/\";:£§º©®\s]+[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+|[^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+([\u0020\u00A0][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+){1,3}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+([\u0020\u00A0][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+){1,3}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+([\u0020\u00A0][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+){1,3})$"

@require_GET
def geocode_api(request):
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