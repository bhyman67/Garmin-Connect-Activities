# Loop through all of the gpx files in the "GPX Files" directory and read in the gpx
# data.
from datetime import datetime
import os, re
import gpxpy
import gpxpy.gpx
from geopy.distance import geodesic
import json

def get_total_distance(gpx):
    
    # Initialize total distance
    total_distance = 0.0

    # Iterate through track points and calculate distance
    for track in gpx.tracks:
        for segment in track.segments:
            for i in range(1, len(segment.points)):
                point1 = segment.points[i - 1]
                point2 = segment.points[i]
                coords_1 = (point1.latitude, point1.longitude)
                coords_2 = (point2.latitude, point2.longitude)
                distance = geodesic(coords_1, coords_2).miles
                total_distance += distance

    return total_distance

def get_distance_time(gpx, distance_threshold):

    # Initialize total distance and start time
    total_distance = 0.0
    start_time = None
    elapsed_time = None

    # Iterate through track points and calculate distance
    for track in gpx.tracks:
        for segment in track.segments:
            for i in range(1, len(segment.points)):
                point1 = segment.points[i - 1]
                point2 = segment.points[i]
                coords_1 = (point1.latitude, point1.longitude)
                coords_2 = (point2.latitude, point2.longitude)
                distance = geodesic(coords_1, coords_2).miles
                total_distance += distance

                # Record the start time
                if start_time is None:
                    start_time = point1.time

                # Check if the total distance has reached 5 miles
                if total_distance >= distance_threshold and elapsed_time is None:
                    elapsed_time = point2.time - start_time
                    break

            if elapsed_time is not None:
                break
        if elapsed_time is not None:
            break

    return elapsed_time


# This will be a list of tuples where the first element is the activity ID from
# the file name and the second element will be the lap time in seconds.
GPX_metrics = []

# Get the path to the GPX Files directory and the list of files in the directory
gpx_files_dir = os.path.join("..", "Garmin Activity GPX Data")
gpx_files = os.listdir(gpx_files_dir)

# Loop through all of the GPX files in the directory
for gpx_file in gpx_files:

    # Extract the activity ID from the file name
    match = re.search(r'_(\d+)\.gpx$', gpx_file)
    activity_id = match.group(1)

    # Extract the 5k time out of the gpx file
    with(open(os.path.join(gpx_files_dir, gpx_file), "r")) as gpx:

        gpx = gpxpy.parse(gpx)

        elapsed_time_5k = get_distance_time(gpx, 3.1)
        elapsed_time_10k = get_distance_time(gpx, 6.2)
        total_distance = get_total_distance(gpx)

        GPX_metrics.append(
            (
                activity_id, 
                str(elapsed_time_5k),
                str(elapsed_time_10k),
                str(total_distance)
            )
        )

# Write the 5k times to a JSON file
with open("Activity Metrics from GPX Data.json", "w") as f:
    json.dump(GPX_metrics, f, indent=4)

print("GPX metrics written to 5k_times.json")
