# Loop through all of the gpx files in the "GPX Files" directory and read in the gpx
# data.
from datetime import datetime
import os, re
import gpxpy
import gpxpy.gpx
from geopy.distance import geodesic
import json

# This will be a list of tuples where the first element is the activity ID from
# the file name and the second element will be the lap time in seconds.
time_5k = []

# Get the path to the GPX Files directory
cwd = os.getcwd()
gpx_files_dir = os.path.join(cwd, "GPX Files")

# Get a list of all of the files in the GPX Files directory
gpx_files = os.listdir(gpx_files_dir)
for gpx_file in gpx_files:

    # Extract the activity ID from the file name
    match = re.search(r'_(\d+)\.gpx$', gpx_file)
    activity_id = match.group(1)

    # Extract the 5k time out of the gpx file
    with(open(os.path.join(gpx_files_dir, gpx_file), "r")) as gpx:

        gpx = gpxpy.parse(gpx)

        # Initialize total distance and start time
        total_distance = 0.0
        start_time = None
        elapsed_time_5k = None

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
                    if total_distance >= 3.01 and elapsed_time_5k is None:
                        elapsed_time_5k = point2.time - start_time
                        break

                if elapsed_time_5k is not None:
                    break
            if elapsed_time_5k is not None:
                break

        if elapsed_time_5k is not None:
            #print(f"Elapsed time to reach 5 miles: {elapsed_time_5k}")
            time_5k.append((activity_id, str(elapsed_time_5k)))
        else:
            #print("5 miles not reached in the provided GPX data.")
            time_5k.append((activity_id, None))

# Write the 5k times to a JSON file
with open("Distance Times/5k_times.json", "w") as f:
    json.dump(time_5k, f)

print("5k times written to 5k_times.json")
