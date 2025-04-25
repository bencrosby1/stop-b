from django.views.generic import TemplateView
from django.http import HttpResponseBadRequest
from django.conf import settings
import requests

class Directions(TemplateView):
    template_name = "directions.html"

    def get(self, request, *args, **kwargs):
        # Only require a destination parameter.
        destination_input = request.GET.get('destination', '').strip()
        if not destination_input:
            return HttpResponseBadRequest("The 'destination' parameter is required.")

        destination_coords = parse_location(destination_input)
        if not destination_coords:
            return HttpResponseBadRequest("Invalid destination location provided.")

        context = self.get_context_data(**kwargs)
        context.update({
            "destination": destination_input,
            "destination_coords": destination_coords,  # (lat, lng) tuple
            "google_maps_api_key": settings.MAPS_API_KEY,
        })
        return self.render_to_response(context)


def parse_location(location_str):
    # Attempt to parse a "lat,lng" string.
    if ',' in location_str:
        try:
            return tuple(map(float, location_str.split(',')))
        except ValueError:
            pass
    # Otherwise, try to geocode it.
    return geocode_address(location_str)


def geocode_address(address):
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": settings.MAPS_API_KEY}
    response = requests.get(geocode_url, params=params)
    if response.status_code == 200:
        result = response.json()
        if result.get("status") == "OK" and result.get("results"):
            loc = result["results"][0]["geometry"]["location"]
            return (loc["lat"], loc["lng"])
    return None
