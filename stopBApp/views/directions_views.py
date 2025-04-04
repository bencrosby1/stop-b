from django.views import View
import requests
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.conf import settings

class Directions(View):
    def get(self, request):
        origin_input = request.GET.get('origin', '').strip()
        destination_input = request.GET.get('destination', '').strip()

        if not origin_input or not destination_input:
            return HttpResponseBadRequest("Both 'origin' and 'destination' parameters are required.")

        origin_coords = parse_location(origin_input)
        destination_coords = parse_location(destination_input)

        if not (origin_coords and destination_coords):
            return HttpResponseBadRequest("Invalid origin or destination location provided.")

        payload = {
            "origin": {"location": {"latLng": {"latitude": origin_coords[0], "longitude": origin_coords[1]}}},
            "destination": {"location": {"latLng": {"latitude": destination_coords[0], "longitude": destination_coords[1]}}},
            "travelMode": "WALK",
            "computeAlternativeRoutes": True
        }
        routes_url = "https://routes.googleapis.com/directions/v2:computeRoutes"
        params = {"key": settings.MAPS_API_KEY}
        headers = {"X-Goog-FieldMask": "routes.distanceMeters,routes.duration,routes.polyline.encodedPolyline"}

        routes_response = requests.post(routes_url, params=params, json=payload, headers=headers)
        if routes_response.status_code != 200:
            return HttpResponseBadRequest("Routes API error: " + routes_response.text)
        
        routes_data = routes_response.json()
        if "error" in routes_data or not routes_data.get("routes", []):
            return HttpResponseBadRequest("Routes API error: " +
                                          routes_data.get("error", {}).get("message", "No routes found."))
        encoded_polyline = routes_data["routes"][0].get("polyline", {}).get("encodedPolyline", "")

        context = {
            "origin": origin_input,
            "destination": destination_input,
            "route_polyline": encoded_polyline,
            "google_maps_api_key": settings.MAPS_API_KEY,
            "origin_coords": origin_coords,
            "destination_coords": destination_coords,
        }
        return render(request, "directions.html", context)

def parse_location(location_str):
    if ',' in location_str:
        try:
            return tuple(map(float, location_str.split(',')))
        except ValueError:
            pass
    return geocode_address(location_str)

def geocode_address(address):
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": settings.MAPS_API_KEY}
    response = requests.get(geocode_url, params=params)
    if response.status_code == 200:
        result = response.json()
        if result.get("status") == "OK" and result.get("results"):
            loc = result["results"][0]["geometry"]["location"]
            return loc["lat"], loc["lng"]
    return None