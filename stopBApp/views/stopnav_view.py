from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils.timezone import now
from stopBApp.models import Location
import os
import json
import pandas as pd

from stopBApp.views.bus_times_views import GTFS_FOLDER, stops_df

GTFS_FOLDER = os.path.join(os.path.dirname(__file__), "../../gtfs_data")

stops_df = pd.read_csv(os.path.join(GTFS_FOLDER, "stops.txt"))

stops_df["stop_lat"] = stops_df["stop_lat"].astype(float)
stops_df["stop_lon"] = stops_df["stop_lon"].astype(float)

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
        try:
            stops = get_bus_stops()
            return render(request, 'navigation.html', {
                'google_maps_api_key': settings.MAPS_API_KEY,
                'bus_stops': json.dumps(stops),
                'default_center': json.dumps({'lat': 43.0389, 'lng': -87.9065}) #mil coords
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)

def get_bus_stops():
    return [
        {
            'id': row['stop_id'],
            'name': row['stop_name'],
            'lat': row['stop_lat'],
            'lng': row['stop_lon'],
            'routes': []
        }
        for _, row in stops_df.iterrows()
    ]