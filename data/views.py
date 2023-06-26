# HTTP Request: GET {{baseURL}}/api/data/ons
# Query Parameters: district (string)

from django.http import JsonResponse
from main_app.models import StaticOnsData
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='get',
    operation_summary='Get ONS data for a district',
    manual_parameters=[
        openapi.Parameter(
            name='query',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='The name of the district to retrieve data for.',
            required=True,
        ),
    ],
    responses={
        200: openapi.Response(
            description='Successful data retrieval',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(
                        type=openapi.TYPE_STRING
                    ),
                },
            ),
        ),
        400: openapi.Response(
            description='Invalid input or data retrieval error',
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