import pandas as pd

path = "/Users/leofeingold/Desktop/pybaseball/stuff+_statcast_data.csv"
df = pd.read_csv(path)

# Basic data inspection
print(df.head())
print(df.info())
print(df.describe())

# Check for NaN values
nan_summary = df.isna().sum()
print("NaN values per column:\n", nan_summary)
