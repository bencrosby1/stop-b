import os
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_GET

@require_GET
def get_stop_coordinates(request):
    stop_id = request.GET.get("stop_id")
    if not stop_id:
        return JsonResponse({"error": "Missing stop_id parameter"}, status=400)

    stops_path = os.path.join(settings.BASE_DIR, "gtfs_data", "stops.txt")
    try:
        with open(stops_path, "r") as f:
            for line in f:
                fields = line.strip().split(",")
                # fields: [lat, id, lon, …]
                if fields[1] == stop_id:
                    return JsonResponse({
                        "lat": float(fields[0]),
                        "lon": float(fields[2]),
                    })
    except OSError:
        return JsonResponse({"error": "Could not load stops file"}, status=500)

    return JsonResponse({"error": "Stop ID not found"}, status=404)
