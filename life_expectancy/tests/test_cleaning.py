"""Tests for the cleaning module"""
import pandas as pd
import pytest

from life_expectancy.cleaning import clean_data
from . import OUTPUT_DIR

@pytest.fixture
def region(request):
    return request.config.getoption("--region")

def test_clean_data(pt_life_expectancy_expected, region):
    """Run the `clean_data` function and compare the output to the expected output"""
    
    clean_data(region)
    pt_life_expectancy_actual = pd.read_csv(
        OUTPUT_DIR / "pt_life_expectancy.csv"
    )
    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )

