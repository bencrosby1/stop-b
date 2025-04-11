from django.shortcuts import render
from stopBApp.models import Detour
from django.http import JsonResponse

def active_detours(request):
    """
    View to display active detours.
    Supports both HTML rendering and JSON responses for AJAX requests.
    (do not know where we are adding this too so implemented functionality for both)
    """
    detours = Detour.objects.filter(is_active=True)
    # check if request is AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        detours_data = [
            {
                'title': Detour.title,
                'description': Detour.description,
                'start_date': Detour.start_date.strftime('%Y-%m-%d %H:%M:%S'),
                'end_date': Detour.end_date.strftime('%Y-%m-%d %H:%M:%S'),
                'affected_lines': [line.name for line in Detour.affected_lines.all()],
            }
            for Detour in detours
        ]
        return JsonResponse({"detours": detours_data})
    
    # default rendering for HTML Template
    return render(request, 'detours_view.html', {'detours': detours})