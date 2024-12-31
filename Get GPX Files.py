import os
import pandas as pd
from retrieve_creds import retrieve_creds
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
    GarminConnectConnectionError
)

# Setup Garmin Connect client object with credentials
username, password = retrieve_creds('garmin connect/explore')
client = Garmin(username, password)

# Attempt to login
try:
    client = Garmin(username, password)
    client.login()
    print("Login successful!")
except GarminConnectAuthenticationError:
    print("Authentication error. Check your credentials.")
except GarminConnectTooManyRequestsError:
    print("Too many requests. Try again later.")
except GarminConnectConnectionError:
    print("Connection error. Check your internet connection.")

# Get all activities from the pickle file
activities = pd.read_pickle('Garmin 945 Activities Raw.pkl')

# filter activityType down to these activities: Running, Treadmill Running, Trail Running
activities['activityType'] = activities['activityType'].apply(lambda x: x.get('typeKey') if isinstance(x, dict) else None)
activities = activities[activities['activityType'].isin(['running', 'trail_running'])]

activity_download_count = input("How many of activity GPX files would you like to download?") 
activity_download_count = int(activity_download_count)
for i in range(len(activities)):

    # check if the activity has already been downloaded
    activity_id = activities['activityId'].iloc[i]
    activity_name = activities['activityName'].iloc[i]
    activity_start_time_local = activities['startTimeLocal'].iloc[i]
    # replace any colons in the activity start time local underscores
    activity_start_time_local = activity_start_time_local.replace(":", "_")
    activity_gpx_name = f"{activity_name}_{activity_start_time_local}_{activity_id}.gpx"

    if activity_download_count == 0:
        break
    elif activity_gpx_name in os.listdir("GPX Files"):
        print(f"{activity_name} has already been downloaded. Skipping...")
        continue

    print(f"Downloading {activity_name}...")

    # Get the GPX file
    gpx = client.download_activity(activity_id, dl_fmt=Garmin.ActivityDownloadFormat.GPX)

    # Save the GPX file
    with open(os.path.join("GPX Files", activity_gpx_name), "wb") as f:
        f.write(gpx)
    print(f"Downloaded {activity_name}.gpx")

    activity_download_count -= 1

print("Done!")