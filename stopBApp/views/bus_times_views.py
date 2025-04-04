import pandas as pd
import os
from datetime import datetime
from django.shortcuts import render
from math import radians, sin, cos, sqrt, atan2
from django.http import JsonResponse


GTFS_FOLDER = os.path.join(os.path.dirname(__file__), "../../gtfs_data")

calendar_dates_df = pd.read_csv(os.path.join(GTFS_FOLDER, "calendar_dates.txt"))

#load to get bus stop arrival times
stop_times_df = pd.read_csv(os.path.join(GTFS_FOLDER, "stop_times.txt"))
#load to get route IDs and their short names
routes_df = pd.read_csv(os.path.join(GTFS_FOLDER, "routes.txt"))

stops_df = pd.read_csv(os.path.join(GTFS_FOLDER, "stops.txt"))

stops_df["stop_lat"] = stops_df["stop_lat"].astype(float)
stops_df["stop_lon"] = stops_df["stop_lon"].astype(float)



trips_df = pd.read_csv(os.path.join(GTFS_FOLDER, "trips.txt"))

def bus_times_page(request):

    return render(request, "bus_times.html")


def get_bus_times(request, stop_id):
    try:
        # convert stop_id from string to integer
        stop_id = int(stop_id)

        today = datetime.today().strftime("%Y%m%d")

        #  service_ids that are active today
        active_services = calendar_dates_df[
            (calendar_dates_df["date"] == int(today)) &
            (calendar_dates_df["exception_type"] == 1)
        ]["service_id"].tolist()

        # Filter trips.txt to only include trips with a service_id that's active today
        valid_trips = trips_df[trips_df["service_id"].isin(active_services)]

        # Filter stop_times.txt for rows where stop_id matches the one the user entered
        stop_times = stop_times_df[stop_times_df["stop_id"] == stop_id][["trip_id", "arrival_time"]]

        # get route_id info for each trip
        stop_times = stop_times.merge(valid_trips[["trip_id", "route_id"]], on="trip_id")


        stop_times = stop_times.merge(routes_df[["route_id", "route_short_name"]], on="route_id")

        # keep only route name and arrival time remove duplicates
        stop_times = stop_times[["route_short_name", "arrival_time"]].drop_duplicates()

        #helper function to convert "24:xx:xx" or higher to "00:xx:xx" format for python
        def normalize_time(t):
            h, m, s = map(int, t.split(":"))
            h = h % 24
            return f"{h:02}:{m:02}:{s:02}"


        stop_times["arrival_time"] = stop_times["arrival_time"].apply(normalize_time)

        stop_times["arrival_time"] = pd.to_datetime(stop_times["arrival_time"], format="%H:%M:%S")

        # current time and filter out any arrivals that have already passed, no old arrivals
        now = datetime.now().time()
        stop_times = stop_times[stop_times["arrival_time"].dt.time > now]

        # remaining arrival times into 12-hour format with AM/PM
        stop_times["arrival_time"] = stop_times["arrival_time"].dt.strftime("%I:%M %p")

        # sort by arrival time and take the first 20 upcoming buses
        stop_times = stop_times.sort_values("arrival_time")
        bus_times = stop_times.head(20).to_dict(orient="records")


        return JsonResponse(bus_times, safe=False)


    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_nearby_stops(request):
    try:
        lat = float(request.GET.get("lat"))
        lon = float(request.GET.get("lon"))

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371
            dlat = radians(lat2 - lat1)
            dlon = radians(lon2 - lon1)
            a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
            return R * 2 * atan2(sqrt(a), sqrt(1 - a))

        nearby = []
        for _, row in stops_df.iterrows():
            d = haversine(lat, lon, row["stop_lat"], row["stop_lon"])
            if d < 5.0:
                nearby.append({
                    "stop_id": row["stop_id"],
                    "stop_name": row["stop_name"],
                    "stop_lat": row["stop_lat"],
                    "stop_lon": row["stop_lon"],
                    "distance": round(d * 1000)
                })

        return JsonResponse(sorted(nearby, key=lambda x: x["distance"]), safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)