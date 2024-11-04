
import pytest
import pandas as pd
from functions import scrub_data

import warnings

# Suppress specific deprecation warnings from libraries you do not control
warnings.filterwarnings("ignore", category=DeprecationWarning, module="plotly.*")


@pytest.fixture
def data():
    # Load the DataFrame from a CSV or define it directly
    df = pd.read_csv('output/datasets/dataset.csv',low_memory=False)
    # Apply any necessary preprocessing you typically use before tests
    df = scrub_data(df)  # Assuming 'scrub_data' is a function you use to clean data
    return df

def test_no_missing_values(data):  # 'data' fixture is used here
    for column in ['latitude', 'longitude', 'date/time']:
        assert not data[column].isnull().any(), f"{column} contains null values"

def test_reasonable_number_of_rows(data):
    assert len(data) > 100, "Data might be too limited after cleaning"

def test_data_types(data):
    assert pd.api.types.is_numeric_dtype(data['number_of_persons_injured']), "Number of persons injured is not numeric"
    assert pd.api.types.is_datetime64_any_dtype(data['date/time']), "Date/time is not a datetime type"

def test_geographical_bounds(data):
    assert data['latitude'].between(40.4, 41.0).all(), "Latitude out of NYC bounds"
    assert data['longitude'].between(-74.3, -73.7).all(), "Longitude out of NYC bounds"
