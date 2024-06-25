from pybaseball import statcast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from pybaseball import cache
cache.enable()


dateInitial = '2023-6-1'
dateEnd = '2024-06-1'

def scrapeData(start, end):
    warnings.simplefilter(action='ignore', category=FutureWarning)
    data = statcast(start_dt = start, end_dt = end)
    data.to_csv("2023-6-1To2024-06-1.csv")
    return data

def loadData(csv):
    df = pd.read_csv(csv)
    return df

def sortData(df):
    # Create a count column
    df['count'] = df['balls'].astype(str) + '-' + df['strikes'].astype(str)

    # Replace 'hit_into_play' descriptions with corresponding 'events'
    df.loc[df['description'] == 'hit_into_play', 'description'] = df['events']

    # Group by the updated description and count, then calculate the mean of delta_run_exp
    mean_delta_run_exp = df.groupby(['description', 'count'])['delta_run_exp'].mean().reset_index()
    mean_delta_run_exp.columns = ['description', 'count', 'mean_delta_run_exp']

    return df, mean_delta_run_exp

def visualizeData(df):
    home_run_data = df[df['description'] == 'home_run']
    plt.figure(figsize=(10, 6))
    plt.bar(home_run_data['count'], home_run_data['mean_delta_run_exp'], color='blue')
    plt.xlabel('Count')
    plt.ylabel('Mean Delta Run Expectancy')
    plt.title('Mean Delta Run Expectancy for Home Runs by Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def mergeData(df, sorted_df):
    df_with_mean_exp = pd.merge(df, sorted_df, on=['description', 'count'], how='left')
    return df_with_mean_exp

def main():
    #data = scrapeData(start=dateInitial, end=dateEnd)
    csv = "/Users/leofeingold/Desktop/pybaseball/Stuff Metric/2023-6-1To2024-06-1.csv"
    df = loadData(csv)
    df, df_sorted = sortData(df)
    df_sorted.to_csv("test.csv")
    visualizeData(df_sorted)
    good_df = mergeData(df, df_sorted)


if __name__ == "__main__":
    main()