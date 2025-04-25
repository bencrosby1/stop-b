from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from stopBApp.models import SavedBusLine, BusLine

@login_required
def save_bus_line(request, bus_line_id):
    """
    Save a bus line for the logged-in user.
    """
    if request.method == "POST":
        # Ensure route_id is treated as a string
        bus_line = get_object_or_404(BusLine, route_id=str(bus_line_id))
        saved_bus_line, created = SavedBusLine.objects.get_or_create(user=request.user, bus_line=bus_line)
        if created:
            return JsonResponse({"message": "Bus line saved successfully!", "name": bus_line.name, "route_id": bus_line.route_id})
        return JsonResponse({"message": "Bus line is already saved.", "name": bus_line.name, "route_id": bus_line.route_id})
    return JsonResponse({"error": "Invalid request method."}, status=400)

@login_required
def unsave_bus_line(request, bus_line_id):
    """
    Unsave a bus line for the logged-in user.
    """
    if request.method == "POST":
        # Ensure route_id is treated as a string
        saved_bus_line = SavedBusLine.objects.filter(user=request.user, bus_line__route_id=str(bus_line_id))
        if saved_bus_line.exists():
            saved_bus_line.delete()
            return JsonResponse({"message": "Bus line unsaved successfully!", "name": bus_line_id})
        return JsonResponse({"message": "Bus line was not saved.", "name": bus_line_id}, status=404)
    return JsonResponse({"error": "Invalid request method."}, status=400)

@login_required
def saved_lines(request):
    """
    View to display all bus lines and the user's saved bus lines.
    """
    # Fetch all bus lines
    all_bus_lines = BusLine.objects.all()

    # Fetch saved bus lines for the logged-in user
    saved_bus_lines = SavedBusLine.objects.filter(user=request.user).select_related('bus_line')

    # Extract the IDs of saved bus lines for easier comparison in the template
    saved_bus_line_ids = saved_bus_lines.values_list('bus_line__id', flat=True)

    return render(request, 'saved_lines.html', {
        'all_bus_lines': all_bus_lines,
        'saved_bus_line_ids': saved_bus_line_ids,
    })