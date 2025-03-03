from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from stopBApp.models import Location
import json

@csrf_exempt
def location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            Location.objects.create(latitude=latitude, longitude=longitude, timestamp=now())
            return JsonResponse({'status': 'success', 'latitude': latitude, 'longitude': longitude})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    elif request.method == 'GET':
        return render(request, 'navigation.html')
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)
