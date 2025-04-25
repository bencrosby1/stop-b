import requests
import xml.etree.ElementTree as ET
from stopBApp.models import BusLine
from decouple import config

def sync_bus_lines():
    """
    Fetch bus lines from the MCTS API and sync them with the database.
    """
    API_KEY = config("API_KEY")  # Store your API key in a `.env` file
    url = f"https://realtime.ridemcts.com/bustime/api/v3/getroutes?key={API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        root = ET.fromstring(response.content)

        # Parse and save bus lines
        for route in root.findall(".//route"):
            route_id = route.find("rt").text
            route_name = route.find("rtnm").text
            description = route.find("rtclr").text if route.find("rtclr") is not None else None

            # Update or create the bus line in the database
            BusLine.objects.update_or_create(
                route_id=route_id,
                defaults={"name": route_name, "description": description},
            )
        print("Successfully synced bus lines from the MCTS API.")
    except requests.RequestException as e:
        print(f"Failed to fetch bus lines from the MCTS API: {e}")
    except ET.ParseError as e:
        print(f"Failed to parse XML response from the MCTS API: {e}")