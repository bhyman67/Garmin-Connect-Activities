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

# Retrieve up to 5,000 activities
activities = client.get_activities(0, 5000)
activities_df = pd.DataFrame(activities)
activities_df.to_pickle('Garmin 945 Activities Raw.pkl')

# The advantage of using the pickle format is that it preserves the DataFrame structure and data types
# The data is saved in a serialized format, which can be read back into a DataFrame without losing 
# any information

input("Done, press Enter to continue...")