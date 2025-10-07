from datetime import timedelta
import pandas as pd
import math

# Function to convert seconds to HH:MM:SS format
def convert_to_elapsed_time(seconds):

    return str(timedelta(seconds=seconds))

# Function to add average weight per rep to each dictionary in the list
def add_avg_weight_per_rep(exercise_sets):
    
    # check if the exercise_sets is a list
    if type(exercise_sets) is not list:
        return None
    
    for exercise in exercise_sets:
        if exercise['reps'] > 0:
            exercise['avg_weight_per_rep'] = math.ceil(exercise['volume'] * 0.00220462) / exercise['reps'] 
        else:
            exercise['avg_weight_per_rep'] = 0

    return exercise_sets

# Load the raw activities data from the pickle file
activities_df = pd.read_pickle('Garmin 945 Activities Raw.pkl')

# DATA PREP ==> Cleaning/Transforming/Formating
activities_df['duration'] = activities_df['duration'].fillna(0).apply(convert_to_elapsed_time)
activities_df['elapsedDuration'] = activities_df['elapsedDuration'].fillna(0).apply(convert_to_elapsed_time)
activities_df['movingDuration'] = activities_df['movingDuration'].fillna(0).apply(convert_to_elapsed_time)
activities_df['activityType'] = activities_df['activityType'].apply(lambda x: x['typeKey'])
activities_df['distance'] = activities_df['distance'].apply(lambda x: x * 0.000621371)
activities_df['activityType'] = activities_df['activityType'].apply(lambda x: x.replace('_', ' ').title())
activities_df['privacy'] = activities_df['privacy'].apply(lambda x: x['typeKey'])
activities_df['minTemperature'] = activities_df['minTemperature'].apply(lambda x: x * 9/5 + 32)
activities_df['maxTemperature'] = activities_df['maxTemperature'].apply(lambda x: x * 9/5 + 32)

# DATA ENRICHMENT ==> Modify summarized exercise sets by adding in average weight lifted per rep
activities_df['summarizedExerciseSets'] = activities_df['summarizedExerciseSets'].apply(add_avg_weight_per_rep)

# Extract the first item from the list in the 'Summarized Exercise Sets' column
activities_df['First Exercise Set'] = activities_df['summarizedExerciseSets'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else {})

# Normalize the JSON data in the 'First Exercise Set' column
#   -> Drop the category, subcategory, and duration columns
exercise_sets_df = pd.json_normalize(activities_df['First Exercise Set'])
exercise_sets_df.drop(columns=['category', 'subCategory', 'duration'], inplace=True)
exercise_sets_df['volume'] = exercise_sets_df['volume'].fillna(0)
exercise_sets_df['volume'] = exercise_sets_df['volume'].apply(lambda x: math.ceil(x * 0.00220462))

# Add the normalized data to the original DataFrame and drop the 'First Exercise Set' column
activities_df = pd.concat([activities_df, exercise_sets_df], axis=1)
activities_df.drop(columns=['First Exercise Set'], inplace=True)

# Create a DataFrame with the dummy rows
dummy_rows = pd.DataFrame([
    {'activityType': 'Running', 'startTimeLocal': '2022-01-03T00:00:00.000Z', 'distance': 0},
    {'activityType': 'Running', 'startTimeLocal': '2025-12-30T00:00:00.000Z', 'distance': 0}
])
activities_df = pd.concat([activities_df, dummy_rows], ignore_index=True)

# Column headers to rename and select (STORE THIS IN A JSON FILE!!!)
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
    'privacy': 'Privacy Setting',
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
    'reps': 'Reps',
    'volume': 'Volume',
    'sets': 'Sets',
    'avg_weight_per_rep': 'Avg Weight Per Rep',
    'avgVerticalSpeed': 'Avg Vertical Speed',
    'caloriesConsumed': 'Calories Consumed',
    'waterConsumed': 'Water Consumed',
    'minRespirationRate': 'Min Respiration Rate',
    'maxRespirationRate': 'Max Respiration Rate',
    'avgRespirationRate': 'Avg Respiration Rate',
    'avgStress': 'Avg Stress',
    'startStress': 'Start Stress',
    'endStress': 'End Stress',
    'differenceStress': 'Difference Stress',
    'maxStress': 'Max Stress',
    '5k Time': '5k Time'
}

# Loop through all files in the "GPX Files" directory and extract the time it took to complete a 5k run
run_5k_times = pd.read_json('Activity Metrics from GPX Data.json', orient='records')
run_5k_times.columns = ['activityId', '5k Time', '10k Time', 'Total Distance']
# join with the activities_df DataFrame on the 'activityId' column
activities_df = activities_df.merge(run_5k_times, how='left', on='activityId')

# Subset the data to only show the columns we want
activities_df = activities_df[renaming_dict.keys()]

# Rename the columns
activities_df.rename(columns=renaming_dict, inplace=True)

# Save the data to a CSV file in the parent directory
activities_df.to_csv('../Garmin 945 Activities.csv', index=False)

input("Data has been saved to Garmin 945 Activities.csv.")