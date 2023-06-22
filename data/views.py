from django.http import JsonResponse
from django.views.decorators.http import require_GET
from main_app.models import StaticOnsData

@require_GET
def ons(request):
    query = request.GET.get('query')
    if query:
        try:
            stats = StaticOnsData.objects.filter(district=query)
            data = []
            for stat in stats:
                data_point = {
                    'date': stat.date,
                    'district': stat.district
                }
                for field_name, field_value in stat.__dict__.items():
                    if field_name not in ['date', 'district', '_state']:
                        data_point[field_name] = field_value
                data.append(data_point)
            return JsonResponse({'data': data}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)