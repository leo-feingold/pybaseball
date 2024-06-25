# I want to add the number of strikes vs balls on taken pitches

import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import warnings
from pybaseball import statcast_batter
from pybaseball import playerid_lookup

dateInitial = '2024-03-28'
dateEnd = '2024-06-4'
firstName = 'Aaron'.title()
lastName = 'Judge'.title()

def getData(nameFirst, nameLast, startDate, endDate):
    warnings.simplefilter(action='ignore', category=FutureWarning)
    player = playerid_lookup(nameLast, nameFirst)
    player_ID = player.loc[0, "key_mlbam"]
    data = statcast_batter(startDate, endDate, player_ID)
    averageBatSpeed = data["bat_speed"].mean()
    return data, averageBatSpeed

def filterData(df, averageBatSpeed):
    twoStrike_df = df[(df["strikes"] == 2) & ((df["balls"] == 0) | (df["balls"] == 1))][['delta_run_exp', 'bat_speed', 'swing_length', 'pitch_type', 'game_date']]
    dfSwings = twoStrike_df.dropna(subset=['bat_speed'])
    dfTakes = twoStrike_df[twoStrike_df['bat_speed'].isnull()]
    meanRVTake = dfTakes['delta_run_exp'].mean()
    numAgroSwings = len(dfSwings[dfSwings['bat_speed'] > averageBatSpeed])
    meanRVAgroSwing = dfSwings[dfSwings['bat_speed'] > averageBatSpeed]['delta_run_exp'].mean()
    meanRVPassiveSwing = dfSwings[dfSwings['bat_speed'] < averageBatSpeed]['delta_run_exp'].mean()
    return dfSwings, dfTakes, meanRVTake, meanRVAgroSwing, meanRVPassiveSwing, numAgroSwings

def visualizeData(swings, takes, meanTake, meanAgroSwing, averageBatSpeed, meanRVPassiveSwing, numAgroSwings):
    fig, axs = plt.subplots()
    axs.scatter(swings["bat_speed"], swings["delta_run_exp"], label = "Swings", color = 'green')
    axs.axhline(y=meanTake, color='blue', linestyle='--', label=f"Mean Take Run Value: ({meanTake:.3f})")
    axs.axhline(y=meanAgroSwing, color='red', linestyle='--', label=f"Mean Aggressive Swing Run Value: ({meanAgroSwing:.3f})")
    #axs.axvline(x=averageBatSpeed, color='purple', linestyle='--', label=f"Mean Bat Speed: ({averageBatSpeed:.3f})")
    #axs.axhline(y=swings["delta_run_exp"].mean(), color='pink', linestyle='--', label = f'Mean Swing Run Value: ({swings["delta_run_exp"].mean():.3f})')
    axs.axhline(y=meanRVPassiveSwing, color='black', linestyle='--', label=f"Mean Passive Swing Run Value: ({meanRVPassiveSwing:.3f})")
    axs.set_xlabel(f"Bat Speed")
    axs.set_ylabel(f"Delta Run Expectancy")
    plt.suptitle(f"0-2 and 1-2 Counts: {firstName} {lastName} Passive vs Aggressive Swings")
    axs.set_title(f"Average Bat Speed: {averageBatSpeed:.3f}, Number of Swings: {len(swings)} ({numAgroSwings} Aggressive) , Number of Takes: {len(takes)}")
    plt.legend()
    plt.show()

def main():
    data, averageBatSpeed = getData(firstName, lastName, dateInitial, dateEnd)
    swings, takes, meanRVTake, meanRVAgroSwing, meanRVPassiveSwing, numAgroSwings = filterData(data, averageBatSpeed)
    print(f"Swings Shape: {swings.shape}")
    print(f"Takes Shape: {takes.shape}")
    visualizeData(swings, takes, meanRVTake, meanRVAgroSwing, averageBatSpeed, meanRVPassiveSwing, numAgroSwings)

if __name__ == "__main__":
    main()