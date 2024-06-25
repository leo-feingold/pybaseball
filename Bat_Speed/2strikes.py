from pybaseball import statcast
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import warnings

dateInitial = '2024-05-30'
dateEnd = '2024-06-4'


def scrapeData(start, end):
    warnings.simplefilter(action='ignore', category=FutureWarning)
    data = statcast(start_dt = start, end_dt = end)
    return data

def filterData(df):
    df["twoStrikes"] = df["strikes"] == 2
    df = df[['twoStrikes', 'delta_run_exp', 'bat_speed', 'swing_length', 'pitch_type', 'game_date', 'batter', 'type']]
    condition = df.twoStrikes == True
    df = df.loc[condition]
    dfSwings = df.dropna()
    dfTakes = df[df['bat_speed'].isnull()]
    meanRVTake = dfTakes['delta_run_exp'].mean()
    meanRVAgroSwing = dfSwings.loc["bat_speed" >= 70]

    return dfSwings, meanRVTake, meanRVAgroSwing

def visualizeData(df1, meanRVTake, meanRVAgroSwing):
    fig, axs = plt.subplots()
    axs.scatter(df1["bat_speed"], df1["delta_run_exp"], label = "Swings", color = 'green')
    axs.axhline(y=meanRVTake, color='red', linestyle='--', label=f"Mean Take Run Value: ({meanRVTake:.2f})")
    axs.axhline(y=meanRVAgroSwing, color='blue', linestyle='--', label=f"Mean Agressive Swing Run Value: ({meanRVAgroSwing:.2f})")
    axs.set_xlabel(f"Bat Speed")
    axs.set_ylabel(f"Delta Run Expectancy")
    axs.set_title(f"2-Strike Counts: Passive vs Aggressive Swings")
    plt.legend()
    plt.show()


def main():
    data = scrapeData(dateInitial, dateEnd)
    swings, takes, agroSwing = filterData(data)
    visualizeData(swings, takes, agroSwing)


if __name__ == "__main__":
    main()