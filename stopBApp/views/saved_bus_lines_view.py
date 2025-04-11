import requests
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from stopBApp.models import SavedBusLine, BusLine
from decouple import config

API_KEY = config("API_KEY")
url = f"https://realtime.ridemcts.com/bustime/api/v3/getroutes?key={API_KEY}"

@login_required
def saved_bus_lines(request):
    """
    View to display saved bus lines for a logged-in user.
    Fetches all bus lines from the MCTS API and excludes saved ones.
    (do not know where we are adding this too so implemented functionality for both AJAX and HTML rendering)
    """
    # Fetch saved bus lines for the logged-in user
    saved_bus_lines = SavedBusLine.objects.filter(user=request.user).select_related('bus_line')

    # Fetch all bus lines from the MCTS API
    try:
        response = requests.get(url)  # Replace with the actual MCTS API URL
        response.raise_for_status()
        all_bus_lines_data = response.json().get("bustime-response", {}).get("route", [])  # Assuming the API returns JSON data
    except requests.RequestException as e:
        return JsonResponse({"error": "Failed to fetch bus lines from the MCTS API."}, status=500)

    # Filter out saved bus lines
    saved_bus_line_ids = saved_bus_lines.values_list('bus_line__name', flat=True)  # Match by route name
    all_bus_lines = [
        {"id": line["rt"], "name": line["rtnm"]}
        for line in all_bus_lines_data
        if line["rtnm"] not in saved_bus_line_ids
    ]

    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        saved_data = [
            {
                "id": saved.bus_line.id,
                "name": saved.bus_line.name,
                "saved_at": saved.saved_at,
            }
            for saved in saved_bus_lines
        ]
        return JsonResponse({"saved_bus_lines": saved_data, "all_bus_lines": all_bus_lines})

    # Pass both saved and filtered all bus lines to the template
    return render(request, 'saved_bus_lines.html', {
        'saved_bus_lines': saved_bus_lines,
        'all_bus_lines': all_bus_lines
    })

@login_required
def save_bus_line(request, bus_line_id):
    """
    View to save a bus line for the logged-in user.
    """
    if request.method == "POST":
        bus_line = get_object_or_404(BusLine, id=bus_line_id)
        saved_bus_line, created = SavedBusLine.objects.get_or_create(user=request.user, bus_line=bus_line)
        if created:
            return JsonResponse({"message": "Bus line saved successfully!"})
        return JsonResponse({"message": "Bus line is already saved."})
    return JsonResponse({"error": "Invalid request method."}, status=400)

@login_required
def unsave_bus_line(request, bus_line_id):
    """
    View to unsave a bus line for the logged-in user.
    """
    if request.method == "POST":
        saved_bus_line = SavedBusLine.objects.filter(user=request.user, bus_line_id=bus_line_id)
        if saved_bus_line.exists():
            saved_bus_line.delete()
            return JsonResponse({"message": "Bus line unsaved successfully!"})
        return JsonResponse({"message": "Bus line was not saved."}, status=404)
    return JsonResponse({"error": "Invalid request method."}, status=400)