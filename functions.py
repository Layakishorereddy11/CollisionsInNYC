 
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
from sodapy import Socrata
import pandas as pd
# import pandahelper.reports as ph
from datetime import datetime
import urllib


import pandas as pd

def scrub_data(df: pd.DataFrame) -> pd.DataFrame:
    # Parse Date and Time
    df['crash_date'] = pd.to_datetime(df['crash_date']).dt.date  # Ensures only the date part is considered

    # Handling crash_time to ensure only time is considered
    # Assuming 'crash_time' might also include full datetime, we need to isolate the time part.
    if df['crash_time'].str.contains(':').all():  # Simple check if format includes hours and minutes
        df['crash_time'] = pd.to_datetime(df['crash_time'], errors='coerce').dt.time
    else:
        df['crash_time'] = pd.to_datetime(df['crash_time'], format='%H:%M', errors='coerce').dt.time

    # Combine date and time into a single datetime column
    # Ensure correct conversion logic
    df['date/time'] = pd.to_datetime(df['crash_date'].astype(str) + ' ' + df['crash_time'].astype(str), errors='coerce')
    df['date/time'] = pd.to_datetime(df['date/time'])

    # Now, check the dtype again
    print(df['date/time'].dtype)


    # Drop rows with NaN in 'latitude' and 'longitude'
    df.dropna(subset=['latitude', 'longitude'], inplace=True)

    # Rename columns: make lowercase and replace spaces with underscores
    df.rename(str.lower, axis='columns', inplace=True)
    df.columns = df.columns.str.replace(' ', '_')

    # Convert strings to numerical data where applicable
    numeric_cols = ['number_of_persons_injured', 'number_of_pedestrians_injured', 'number_of_cyclist_injured',
                    'number_of_motorist_injured', 'number_of_persons_killed', 'number_of_pedestrians_killed',
                    'number_of_cyclist_killed', 'number_of_motorist_killed']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    df[['latitude', 'longitude']] = df[['latitude', 'longitude']].apply(pd.to_numeric, errors='coerce')

    # Filter data to include only NYC metro area
    nyc_bounds = {
        'latitude_min': 40.4, 'latitude_max': 41.0,
        'longitude_min': -74.3, 'longitude_max': -73.7
    }
    df = df[(df['latitude'].between(nyc_bounds['latitude_min'], nyc_bounds['latitude_max'])) &
            (df['longitude'].between(nyc_bounds['longitude_min'], nyc_bounds['longitude_max']))]
    
    return df
