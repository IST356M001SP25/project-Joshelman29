import os
import pandas as pd
from typing import List, Union


def load_and_filter_storm_data(csv_path: str, columns: List[str]) -> pd.DataFrame:
    """
    Loads storm data from a CSV file and selects only the specified columns.

    Args:
        csv_path (str): Path to the local CSV file.
        columns (List[str]): List of column names to retain.

    Returns:
        pd.DataFrame: Filtered DataFrame with selected columns.
    """
    print(f"Reading and filtering data from {csv_path}...")
    df = pd.read_csv(csv_path, low_memory=False)
    
    missing_cols = [col for col in columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing expected columns in data: {missing_cols}")

    return df[columns]


def save_filtered_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Saves a filtered DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        output_path (str): Path where the CSV should be saved.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Filtered data saved to {output_path}")


def convert_damage_column(col: Union[pd.Series, list]) -> pd.Series:
    """
    Converts storm damage values like "150.00K" or "1.2M" to float in USD.

    Args:
        col (Union[pd.Series, list]): A pandas Series or list of string values representing damage.

    Returns:
        pd.Series: A pandas Series of floats with values converted to USD.
    """
    def parse_value(value: str) -> float:
        if pd.isna(value):
            return 0.0
        value = value.strip().upper()
        if value.endswith('K'):
            return float(value[:-1]) * 1_000
        elif value.endswith('M'):
            return float(value[:-1]) * 1_000_000
        else:
            try:
                return float(value)
            except ValueError:
                return 0.0  # Fallback for unexpected values

    return pd.Series([parse_value(v) for v in col])


def filter_valid_state_fips(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters the DataFrame to retain only rows where STATE_FIPS is between 1 and 53 (inclusive).

    Args:
        df (pd.DataFrame): DataFrame containing a 'STATE_FIPS' column (can be string or int).

    Returns:
        pd.DataFrame: Filtered DataFrame with valid U.S. state FIPS codes.
    """
    df['STATE_FIPS'] = pd.to_numeric(df['STATE_FIPS'], errors='coerce')
    return df[(df['STATE_FIPS'] >= 1) & (df['STATE_FIPS'] <= 53)].copy()


def merge_state_coordinates(storm_df: pd.DataFrame, state_csv_path: str) -> pd.DataFrame:
    """
    Left joins the storm data with state coordinate data based on state names.

    Args:
        storm_df (pd.DataFrame): Cleaned storm data containing 'STATE'.
        state_csv_path (str): Path to the CSV file with state info (must contain 'name' and coordinate columns).

    Returns:
        pd.DataFrame: Merged DataFrame with state coordinates.
    """
    state_df = pd.read_csv(state_csv_path)
    state_df["name"] = state_df["name"].str.upper()

    merged_df = pd.merge(
        storm_df,
        state_df,
        how="left",
        left_on="STATE",
        right_on="name"
    )

    return merged_df


def get_storm_data_pipeline() -> None:
    """
    Function to run the storm data pipeline:
    - Loads the storm data (already downloaded)
    - Filters required columns
    - Filters valid U.S. states by FIPS codes (1 to 53)
    - Converts damage columns to float USD
    - Merges state-level coordinate data
    - Saves the cleaned, enriched data
    """
    raw_path = "cache/storm_data_2024.csv"
    filtered_path = "cache/storm_data_2024_filtered.csv"
    state_csv_path = "cache/states.csv"

    required_columns = [
        "STATE", "STATE_FIPS", "YEAR", "MONTH_NAME", "EVENT_TYPE",
        "INJURIES_DIRECT", "INJURIES_INDIRECT", "DEATHS_DIRECT",
        "DEATHS_INDIRECT", "DAMAGE_PROPERTY", "DAMAGE_CROPS"
    ]

    # Step 1: Load and filter relevant columns
    df_filtered = load_and_filter_storm_data(raw_path, required_columns)

    # Step 2: Filter only valid state FIPS codes (1 to 53)
    df_filtered = filter_valid_state_fips(df_filtered)

    # Step 3: Convert damage fields to numeric
    df_filtered["DAMAGE_PROPERTY"] = convert_damage_column(df_filtered["DAMAGE_PROPERTY"])
    df_filtered["DAMAGE_CROPS"] = convert_damage_column(df_filtered["DAMAGE_CROPS"])

    # Step 4: Merge with state coordinate data
    df_filtered = merge_state_coordinates(df_filtered, state_csv_path)

    # Step 5: Save final enriched data
    save_filtered_data(df_filtered, filtered_path)


# Run the pipeline
get_storm_data_pipeline()
