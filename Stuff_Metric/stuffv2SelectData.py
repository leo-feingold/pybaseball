from pybaseball import statcast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from pybaseball import cache
cache.enable()

dateInitial = '2020-7-23'
dateEnd = '2024-06-1'

def scrapeData(start, end):
    warnings.simplefilter(action='ignore', category=FutureWarning)
    print("Scraping data from {} to {}...".format(start, end))
    data = statcast(start_dt=start, end_dt=end)
    csv_path = f"{dateInitial}To{dateEnd}FullStatcastData.csv"
    data.to_csv(csv_path)
    print(f"Data scraped and saved to {csv_path}")
    return data

def loadData(csv):
    try:
        df = pd.read_csv(csv)
        print(f"Data loaded from {csv}. Length: {len(df)}")
        return df
    except FileNotFoundError:
        print(f"File {csv} not found.")
        return None

def sortData(df):
    # Create a count column
    df['count'] = df['balls'].astype(str) + '-' + df['strikes'].astype(str)

    possible_counts = ["0-0", "0-1", "0-2", "1-0", "1-1", "1-2", "2-0", "2-1", "2-2", "3-0", "3-1", "3-2"]
    df = df[df["count"].isin(possible_counts)]



    # Replace 'hit_into_play' descriptions with corresponding 'events'
    df.loc[df['description'] == 'hit_into_play', 'description'] = df['events']

    # Combine similar events
    '''
    ['called_strike' 'foul' 'blocked_ball' 'field_out' 'ball' 'double'
    'swinging_strike' 'single' 'force_out' 'triple' 'home_run' 'foul_tip'
    'sac_bunt' 'swinging_strike_blocked' 'sac_fly' 'double_play'
    'grounded_into_double_play' 'foul_bunt' 'hit_by_pitch' 'field_error'
    'missed_bunt' 'fielders_choice' 'fielders_choice_out' 'catcher_interf'
    'pitchout' 'sac_fly_double_play' 'bunt_foul_tip' 'triple_play']
    '''


    df['description'] = df['description'].replace(['ball', 'blocked_ball'], 'ball')
    df['description'] = df['description'].replace(['swinging_strike', 'swinging_strike_blocked', 'foul_tip'], 'swinging_strike')
    df['description'] = df['description'].replace(['field_out', 'triple_play', 'force_out', 'fielders_choice_out', 'double_play', 'grounded_into_double_play'], 'field_out')

    # Filter relevant descriptions
    relevant_descriptions = ['called_strike', 'foul', 'field_out', 'ball', 'double', 'swinging_strike', 'single', 'triple', 'home_run', 'hit_by_pitch']
    df = df[df['description'].isin(relevant_descriptions)]

    # Group by description and count, then calculate the mean of delta_run_exp
    mean_delta_run_exp = df.groupby(['description', 'count'])['delta_run_exp'].mean().reset_index(drop=False)
    mean_delta_run_exp.columns = ['description', 'count', 'mean_delta_run_exp']

    return df, mean_delta_run_exp

def mergeData(df, sorted_df):
    df_with_mean_exp = pd.merge(df, sorted_df, on=['description', 'count'], how='left')
    return df_with_mean_exp


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


def main():
    #df = scrapeData(start=dateInitial, end=dateEnd)
    csv = "/Users/leofeingold/Desktop/pybaseball/2020-7-23To2024-06-1FullStatcastData.csv"
    df = loadData(csv)
    df, df_sorted = sortData(df)
    visualizeData(df_sorted)
    good_df = mergeData(df, df_sorted)
    print(good_df.description.unique())
    print(good_df[["description", "count", "delta_run_exp", "mean_delta_run_exp"]].head(30))
    print(good_df)
    good_df.to_csv(f"stuff+_statcast_data{dateInitial}To{dateEnd}.csv")


if __name__ == "__main__":
    main()