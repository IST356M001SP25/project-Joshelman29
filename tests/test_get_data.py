import pandas as pd
from code.get_data import load_and_filter_storm_data, convert_damage_column

def test_load_and_filter_storm_data():
    """
    Tests that the filtered storm data:
    - Has the expected number of rows and columns
    - Has the correct column names
    """
    csv_path = "cache/storm_data_2024_filtered.csv"
    expected_columns = [
        "STATE", "STATE_FIPS", "YEAR", "MONTH_NAME", "EVENT_TYPE",
        "INJURIES_DIRECT", "INJURIES_INDIRECT", "DEATHS_DIRECT",
        "DEATHS_INDIRECT", "DAMAGE_PROPERTY", "DAMAGE_CROPS"
    ]
    expected_rows = 63096

    df = load_and_filter_storm_data(csv_path, expected_columns)

    assert df.shape[0] == expected_rows, f"Expected {expected_rows} rows, got {df.shape[0]}"
    assert df.shape[1] == len(expected_columns), f"Expected {len(expected_columns)} columns, got {df.shape[1]}"
    assert list(df.columns) == expected_columns, f"Column names do not match expected list"


def test_convert_damage_column():
    """
    Tests convert_damage_column function for correct numeric conversion from strings like '150.00K' and '1.2M'.
    """
    raw_data = ["150.00K", "1.2M", "0.00K", None, "750.5K", "3.1M", ""]
    expected_output = pd.Series([
        150000.0,
        1200000.0,
        0.0,
        0.0,
        750500.0,
        3100000.0,
        0.0
    ])

    result = convert_damage_column(raw_data)
    pd.testing.assert_series_equal(result, expected_output)
