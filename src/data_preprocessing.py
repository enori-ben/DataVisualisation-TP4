from pathlib import Path
import pandas as pd

# Project paths
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

INPUT_FILE = DATA_DIR / "world_bank_2000_2023.csv"
OUTPUT_FILE = DATA_DIR / "cleaned_world_bank.csv"

# Required columns
REQUIRED_COLUMNS = [
    "ISO3",
    "Country",
    "Region",
    "Income_Group",
    "Year",
    "GDP_Per_Capita",
    "Life_Expectancy",
    "Internet_Users_Pct",
    "Population",
]

NUMERIC_COLUMNS = [
    "Year",
    "GDP_Per_Capita",
    "Life_Expectancy",
    "Internet_Users_Pct",
    "Population",
]


def load_data():
    """Load the original World Bank dataset."""
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)

    missing_columns = [
        col for col in REQUIRED_COLUMNS if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    return df


def clean_data(df):
    """Clean column names, data types and duplicate observations."""

    df = df.copy()

    # Clean text columns
    text_columns = ["ISO3", "Country", "Region", "Income_Group"]

    for col in text_columns:
        df[col] = df[col].astype("string").str.strip()

    # Convert numerical columns
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove rows without country identification
    df = df.dropna(subset=["ISO3", "Country"])

    # Remove aggregate observations without country classification
    df = df.dropna(subset=["Region", "Income_Group"])

    # Remove duplicate country-year observations
    df = df.drop_duplicates(
        subset=["ISO3", "Year"],
        keep="first"
    )

    # Keep observations from the assignment period
    df = df[df["Year"].between(2000, 2023)]

    # Sort observations
    df = df.sort_values(
        by=["Country", "Year"]
    ).reset_index(drop=True)

    return df


def main():
    print("Loading World Bank dataset...")

    original_df = load_data()

    print(f"Original rows: {len(original_df)}")

    cleaned_df = clean_data(original_df)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(OUTPUT_FILE, index=False)

    print("\nData cleaning completed.")
    print(f"Cleaned rows: {len(cleaned_df)}")
    print(f"Countries/Economies: {cleaned_df['ISO3'].nunique()}")
    print(
        f"Year range: {int(cleaned_df['Year'].min())} - "
        f"{int(cleaned_df['Year'].max())}"
    )

    print("\nMissing values:")
    print(cleaned_df[REQUIRED_COLUMNS].isnull().sum())

    print(f"\nCleaned dataset saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
