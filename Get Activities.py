import pandas as pd
import garminconnect as gc
from datetime import timedelta
from retrieve_creds import retrieve_creds

# Function to convert seconds to HH:MM:SS format
def convert_to_elapsed_time(seconds):

    return str(timedelta(seconds=seconds))

# Setup Garmin Connect client obj (login required)
username, password = retrieve_creds('garmin connect/explore')
client = gc.Garmin(username, password)
client.login()

# Get all activities (up to 2000) and convert to a DataFrame
activities = client.get_activities(0, 2000)
activities_df = pd.DataFrame(activities)

# Data Cleaning and Transformation/Formating
activities_df['duration'] = activities_df['duration'].fillna(0).apply(convert_to_elapsed_time)
activities_df['elapsedDuration'] = activities_df['elapsedDuration'].fillna(0).apply(convert_to_elapsed_time)
activities_df['movingDuration'] = activities_df['movingDuration'].fillna(0).apply(convert_to_elapsed_time)
activities_df['activityType'] = activities_df['activityType'].apply(lambda x: x['typeKey'])
activities_df['distance'] = activities_df['distance'].apply(lambda x: x * 0.000621371)
activities_df['activityType'] = activities_df['activityType'].apply(lambda x: x.replace('_', ' ').title())

# Column headers to rename and select
renaming_dict = {
    'activityType': 'Activity Type',
    'activityName': 'Activity Name',
    'locationName': 'Location Name',
    'description': 'Description',
    'startTimeLocal': 'Date',
    'distance': 'Distance (miles)',
    'duration': 'Duration (HH:MM:SS.sss)',
    'elapsedDuration': 'Elapsed Duration (H:MM:SS.sss)',
    'movingDuration': 'Moving Duration (HH:MM:SS.sss)',
    'elevationGain': 'Elevation Gain - meters',
    'elevationLoss': 'Elevation Loss - meters',
    'averageSpeed': 'Average Speed',
    'maxSpeed': 'Max Speed',
    'calories': 'Calories',
    'bmrCalories': 'BMR Calories',
    'averageHR': 'Average HR',
    'maxHR': 'Max HR',
    'averageRunningCadenceInStepsPerMinute': 'Average Running Cadence In Steps Per Minute',
    'maxRunningCadenceInStepsPerMinute': 'Max Running Cadence In Steps Per Minute',
    'steps': 'Steps',
    'privacy': 'Privacy',
    'beginTimestamp': 'Begin Timestamp',
    'aerobicTrainingEffect': 'Aerobic Training Effect',
    'anaerobicTrainingEffect': 'Anaerobic Training Effect',
    'avgStrideLength': 'Avg Stride Length',
    'minTemperature': 'Min Temperature',
    'maxTemperature': 'Max Temperature',
    'minElevation': 'Min Elevation',
    'maxElevation': 'Max Elevation',
    'maxDoubleCadence': 'Max Double Cadence',
    'maxVerticalSpeed': 'Max Vertical Speed',
    'lapCount': 'Lap Count',
    'waterEstimated': 'Water Estimated',
    'trainingEffectLabel': 'Training Effect Label',
    'activityTrainingLoad': 'Activity Training Load',
    'minActivityLapDuration': 'Min Activity Lap Duration',
    'aerobicTrainingEffectMessage': 'Aerobic Training Effect Message',
    'anaerobicTrainingEffectMessage': 'Anaerobic Training Effect Message',
    'moderateIntensityMinutes': 'Moderate Intensity Minutes',
    'vigorousIntensityMinutes': 'Vigorous Intensity Minutes',
    'fastestSplit_1000': 'Fastest Split 1000',
    'pr': 'PR',
    'manualActivity': 'Manual Activity',
    'vO2MaxValue': 'VO2 Max Value',
    'summarizedExerciseSets': 'Summarized Exercise Sets',
    'avgVerticalSpeed': 'Avg Vertical Speed',
    'caloriesConsumed': 'Calories Consumed',
    'waterConsumed': 'Water Consumed',
    'totalSets': 'Total Sets',
    'activeSets': 'Active Sets',
    'totalReps': 'Total Reps',
    'minRespirationRate': 'Min Respiration Rate',
    'maxRespirationRate': 'Max Respiration Rate',
    'avgRespirationRate': 'Avg Respiration Rate',
    'avgStress': 'Avg Stress',
    'startStress': 'Start Stress',
    'endStress': 'End Stress',
    'differenceStress': 'Difference Stress',
    'maxStress': 'Max Stress'
}

# Subset the data to only show the columns we want
activities_df = activities_df[renaming_dict.keys()]

# Rename the columns
activities_df.rename(columns=renaming_dict, inplace=True)

# Save the data to a CSV file in the parent directory
activities_df.to_csv('../Garmin 945 Activities.csv', index=False)

input("Data has been saved to Garmin 945 Activities.csv. Press Enter to exit.")