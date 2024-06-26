from pybaseball import statcast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.simplefilter(action='ignore')
from pybaseball import cache
cache.enable()

date_initial = "2024-1-1"
date_final = "2024-6-24"
season = 2024
#date_final = "2024-6-24"

player_first_name = "Aaron"
player_last_name = "Nola"

def scrape_data(start, end):
    df = statcast(start_dt=start, end_dt=end)
    return df

def clean_data(df):
    df = df[df["game_type"] == "R"]
    df = df[["pitch_type", "player_name", "p_throws", "stand", "estimated_woba_using_speedangle", 'pfx_x', 'pfx_z']]

    pitch_names = {
        'FS': 'Splitter',
        'SI': 'Sinker',
        'FF': 'Four-Seam Fastball',
        'SL': 'Slider',
        'CU': 'Curveball',
        'FC': 'Cutter',
        'ST': 'Sweeping Curve',
        'CH': 'Changeup',
        'PO': 'Pitch Out',
        'KC': 'Knuckle Curve',
        'SV': 'Screwball',
        'EP': 'Eephus',
        'FA': 'Fastball',
        None: 'Unknown'
    }

    df["pitch_type"] = df["pitch_type"].map(pitch_names)

    return df

def calc_xfip_splits(LHH_path, RHH_path, min_IP, name, season):

    LHH_df = pd.read_csv(LHH_path)
    LHH_df = LHH_df[LHH_df["Season"] == season]

    
    RHH_df = pd.read_csv(RHH_path)
    RHH_df = RHH_df[RHH_df["Season"] == season]

    merged_df = pd.merge(LHH_df, RHH_df, on=["Name", "Season", "Tm"], suffixes=["_LHH", "_RHH"])

    merged_df = merged_df[(merged_df["IP_LHH"] >= min_IP) & (merged_df["IP_RHH"] >= min_IP)]
    merged_df = merged_df[merged_df["Name"] == name]


    merged_df["xFIP_Difference"] = abs(merged_df["xFIP_LHH"] - merged_df["xFIP_RHH"])
    merged_df = merged_df.sort_values("xFIP_Difference")

    print(merged_df[["Season", "Name", "xFIP_LHH", "xFIP_RHH", "xFIP_Difference"]])
    xFIP_LHH = merged_df["xFIP_LHH"].values[0]
    xFIP_RHH = merged_df["xFIP_RHH"].values[0]
    return xFIP_LHH, xFIP_RHH


def visualize_data(df, xfip_L, xfip_R):
    player = f"{player_last_name}, {player_first_name}"
    df = df[df["player_name"] == player]

    throws = df["p_throws"].iloc[0] if not df.empty else None
    
    # this is wrong needs to be fixed
    if throws == "L":
        df["pfx_x"] = df["pfx_x"] * -12
    else:
        df["pfx_x"] = df["pfx_x"] * -12
    

    df["pfx_z"] = df["pfx_z"] * 12

    df_lefty_batter = df[df["stand"] == "L"]
    df_righty_batter = df[df["stand"] == "R"]

    lefty_counts = df_lefty_batter["pitch_type"].value_counts(normalize=True) * 100
    righty_counts = df_righty_batter["pitch_type"].value_counts(normalize=True) * 100

    lefty_xwoba = df_lefty_batter.groupby("pitch_type")["estimated_woba_using_speedangle"].mean().fillna(0.000)
    righty_xwoba = df_righty_batter.groupby("pitch_type")["estimated_woba_using_speedangle"].mean().fillna(0.000)

    fig, axes = plt.subplots(2, 2, figsize=(12, 7.5))

    # Lefty batter pitch type percentages
    axes[0, 0].bar(lefty_counts.index, lefty_counts.values, edgecolor='black')
    axes[0, 0].set_title(f'Pitch Types vs Lefty Batters ({len(df_lefty_batter)} Pitches), xFIP: {xfip_L:.2f}')
    axes[0, 0].set_ylabel('Percentage (%)')
    for i, pitch in enumerate(lefty_counts.index):
        axes[0, 0].text(i, lefty_counts[pitch], f'xwOBA: {lefty_xwoba[pitch]:.3f}', ha='center', va='bottom', fontsize=5, bbox=dict(facecolor='white', alpha=0.5))
    axes[0, 0].tick_params(axis='x', rotation=45)

    # Righty batter pitch type percentages
    axes[0, 1].bar(righty_counts.index, righty_counts.values, edgecolor='black')
    axes[0, 1].set_title(f'Pitch Types vs Righty Batters ({len(df_righty_batter)} Pitches), xFIP: {xfip_R:.2f}')
    axes[0, 1].set_ylabel('Percentage (%)')
    for i, pitch in enumerate(righty_counts.index):
        axes[0, 1].text(i, righty_counts[pitch], f'xwOBA: {righty_xwoba[pitch]:.3f}', ha='center', va='bottom', fontsize=5, bbox=dict(facecolor='white', alpha=0.5))
    axes[0, 1].tick_params(axis='x', rotation=45)

    colors = {
        'Four-Seam Fastball': 'blue',
        'Sinker': 'green',
        'Slider': 'red',
        'Curveball': 'purple',
        'Changeup': 'orange',
        'Splitter': 'brown',
        'Cutter': 'pink',
        'Sweeping Curve': 'cyan',
        'Pitch Out': 'grey',
        'Knuckle Curve': 'turquoise',
        'Screwball': 'black',
        'Eephus': 'magenta',
        'Fastball': 'lime',
        'Unknown': 'teal'
    }

    markers = {
        'Four-Seam Fastball': 'o',
        'Sinker': 's',
        'Slider': 'D',
        'Curveball': '^',
        'Changeup': 'v',
        'Splitter': '<',
        'Cutter': '>',
        'Sweeping Curve': 'P',
        'Pitch Out': 'X',
        'Knuckle Curve': '*',
        'Screwball': 'H',
        'Eephus': '8',
        'Fastball': 'p',
        'Unknown': 'h'
    }


    # Lefty batter pitch movement profile
    sns.scatterplot(ax=axes[1, 0], x='pfx_x', y='pfx_z', data=df_lefty_batter, hue='pitch_type', style='pitch_type', palette=colors, markers=markers, s=50)
    axes[1, 0].set_title(f"Pitch Movement Profile vs Lefty Batters (Pitcher's View)")
    axes[1, 0].set_xlabel('Horizontal Movement (in.)')
    axes[1, 0].set_ylabel('Vertical Movement (in.)')
    axes[1, 0].legend(title='Pitch Type', fontsize=5)
    axes[1, 0].grid(True)

    # Righty batter pitch movement profile
    sns.scatterplot(ax=axes[1, 1], x='pfx_x', y='pfx_z', data=df_righty_batter, hue='pitch_type', style='pitch_type', palette=colors, markers=markers, s=50)
    axes[1, 1].set_title(f"Pitch Movement Profile vs Righty Batters (Pitcher's View)")
    axes[1, 1].set_xlabel('Horizontal Movement (in.)')
    axes[1, 1].set_ylabel('Vertical Movement (in.)')
    axes[1, 1].legend(title='Pitch Type', fontsize=5)
    axes[1, 1].grid(True)

    plt.suptitle(f"{player_first_name} {player_last_name} ({throws}HP): LHH and RHH Pitch Mix with xwOBA Against\n(Date Range: {date_initial} through {date_final})")
    #plt.tight_layout()
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

    return df



def main():
    data = scrape_data(date_initial, date_final)
    LHH_path = "/Users/leofeingold/Desktop/pybaseball/Lefty_Righty_Splits_CSV/21Through23LHHAdvanced.csv"
    RHH_path = "/Users/leofeingold/Desktop/pybaseball/Lefty_Righty_Splits_CSV/21Through23RHHAdvanced.csv"
    xFIP_LHH, xFIP_RHH = calc_xfip_splits(LHH_path, RHH_path, 20, f"{player_first_name} {player_last_name}", season)
    cleaned_data = clean_data(data)
    final_df = visualize_data(cleaned_data, xFIP_LHH, xFIP_RHH)

if __name__ == "__main__":
    main()