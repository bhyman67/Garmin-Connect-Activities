# Garmin Connect Activities

## Overview
This repository contains scripts to retrieve and analyze activity data from Garmin Connect. The goal is to provide a way to download, process, and visualize workout data for personal insights and tracking performance over time.

## Features
- Fetch activity data from Garmin Connect
- Process and analyze fitness data
- Export data in user-friendly formats
- Generate summary statistics and visualizations

## Prerequisites
Ensure you have the following installed before using the scripts:
- Python 3.x
- Required Python packages (listed in `requirements.txt`)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/bhyman67/Garmin-Connect-Activities.git
   cd Garmin-Connect-Activities
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
1. Authenticate with Garmin Connect (if required)
2. Run the script to fetch activities:
   ```sh
   python fetch_activities.py
   ```
3. Process and analyze data using available scripts:
   ```sh
   python analyze_data.py
   ```
4. Export results to csv to make it useable by Tableau.

