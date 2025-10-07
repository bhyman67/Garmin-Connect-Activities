<h1>
    <p align="center">Garmin Connect Activities</p>
</h1>

## Overview
This repository contains scripts to retrieve and process activity data from Garmin Connect so that it can be explored and analyzed in Excel and visualized in Tableau: 

* [Tableau Dashboard](https://public.tableau.com/app/profile/brent1746/viz/RunningandResistanceTrainingTracker/Overview) ([Activity Data](https://1drv.ms/x/c/532f03b812e559b6/EQnySg4u6AVCoOtcMKw7TekB8vOiY29yLaXJxuEDQeI2Yw))


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

## Scripts / Usage

### Script Descriptions
1. [Get Activities](01%20-%20Get%20Activities.py)
   - Authenticate with [Garmin Connect](https://pypi.org/project/garminconnect/)
   - Fetch recent activities
   - Save activities data to a pickle file
   - Handle connection and authentication errors
2. [Get GPX Files](02%20-%20Get%20GPX%20Files.py)
3. [Extract GPX Activity Metrics from GPX Files](03%20-%20Extract%20GPX%20Activity%20Metrics.py)
4. [Activity Prep, Transformation, and Enrichment](04%20-%20Activity%20Prep,%20Transformation,%20and%20Enrichment.py)

### Usage

There are two ways to run these scripts. Either all of them sequentially. Or only the first and then the last if you want to skip the GPX piece. 

```mermaid
graph TD
    B[Run Script 01 - Get Activities]
    B --> C[Run Script 04 - Activity Prep, Transformation, and Enrichment]
    C

    B --> D[Run Script 02 - Get GPX Files]
    D --> F[Run Script 03 - Extract GPX Activity Metrics]
    F --> C
```

<p align="right">Click <a href="https://github.com/bhyman67/Garmin-Connect-Activities">here</a> to view the code in this project's repository<p>