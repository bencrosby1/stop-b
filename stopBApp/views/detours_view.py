import requests
import xml.etree.ElementTree as ET
from django.shortcuts import render
from django.http import JsonResponse
from decouple import config
from datetime import datetime

API_KEY = config("API_KEY")
DETOURS_URL = f"https://realtime.ridemcts.com/bustime/api/v3/getdetours?key={API_KEY}"

def active_detours(request):
    try:
        response = requests.get(DETOURS_URL)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        
        detours_data = []
        for detour in root.findall(".//dtr"):
            if detour.find("st").text == "1":  # Only include active detours
                # Convert start_date and end_date to a Django-compatible format
                start_date = datetime.strptime(detour.find("startdt").text, "%Y%m%d %H:%M")
                end_date = datetime.strptime(detour.find("enddt").text, "%Y%m%d %H:%M")
                
                # Remove duplicate route numbers
                routes = list(set(rtdir.find("rt").text for rtdir in detour.findall(".//rtdir")))
                
                detours_data.append({
                    "route": routes,
                    "description": detour.find("desc").text,
                    "start_date": start_date,
                    "end_date": end_date
                })
    except requests.RequestException as e:
        return JsonResponse({"error": "Failed to fetch detours from the MCTS API."}, status=500)
    except ET.ParseError as e:
        return JsonResponse({"error": "Failed to parse XML response from the MCTS API."}, status=500)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({"detours": detours_data})
    
    return render(request, 'active_detours.html', {
        'detours': detours_data
    }) 