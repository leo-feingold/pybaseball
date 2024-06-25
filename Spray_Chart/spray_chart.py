from pybaseball import statcast_batter
import pandas as pd 
import matplotlib.pyplot as plt
from pybaseball import playerid_lookup
import numpy as np
import seaborn as sns
import warnings
import plotly.express as px
import plotly.graph_objects as go

firstName = 'Anthony'.title()
lastName = 'Volpe'.title()
playerTeam = 'yankees'.lower()
playerTeamTag = 'NYY'.upper()
start = '2023-01-01'
stop = '2023-12-31'

def getData(nameFirst, nameLast, startDate, endDate):
    # To get rid of warning in the console:
    warnings.simplefilter(action='ignore', category=FutureWarning)

    player = playerid_lookup(nameLast, nameFirst)
    player_ID = player.loc[0, "key_mlbam"]
    data = statcast_batter(startDate, endDate, player_ID)
    return data

def filterData(df):
    reg_season_condition = df["game_type"] == 'R'
    df = df.loc[reg_season_condition]
    df = df[["home_team", "hc_x", "hc_y", "events", "game_date", "launch_speed", "launch_angle"]]
    df["hit_or_out"] = (df.events == 'single') | (df.events == 'double') | (df.events == 'triple') | (df.events == 'home_run')
    df = df[df["hit_or_out"] == True]
    # To filter only home games
    #df = df[df["home_team"] == playerTeamTag]

    return df

def plotStadium(df, team):
    fig, ax = plt.subplots()
    stadium = pd.read_csv('/Users/leofeingold/Desktop/pybaseball/Spray Chart/mlbstadiums.csv')
    team_df = stadium[stadium['team'] == team.lower()]
    for i in stadium['segment'].unique():
        data = team_df[team_df['segment'] == i]
        ax.plot(data['x'],-1*data['y'], linestyle = '-', color = 'black')
    ax.axis('off')

    color_dict = {
        'single': 'brown',
        'double': 'green',
        'triple': 'blue',
        'home_run': 'black'

    }

    for event, color in color_dict.items():
        subset = df[df['events'] == event]
        ax.scatter(subset.hc_x, -1*subset.hc_y, color=color, label=event, alpha=0.7)

    ax.legend()
    ax.set_title(f"{firstName} {lastName} Spray Chart ({start} - {stop}, Stadium Displayed: {playerTeamTag})")
    plt.show()

def plotStadiumInteractive(df, team):
    df['hc_y'] = df['hc_y'] * -1
    stadium = pd.read_csv('/Users/leofeingold/Desktop/pybaseball/Spray Chart/mlbstadiums.csv')
    team_df = stadium[stadium['team'] == team.lower()]

    stadium_traces = []
    for segment in stadium['segment'].unique():
        data = team_df[team_df['segment'] == segment]
        stadium_trace = go.Scatter(
            x=data['x'],
            y=-1 * data['y'],
            mode='lines',
            line=dict(color='black'),
            showlegend=False
        )
        stadium_traces.append(stadium_trace)

    fig = px.scatter(
        df,
        x='hc_x',
        y='hc_y',
        color='events',
        color_discrete_map={
            'single': 'brown',
            'double': 'green',
            'triple': 'blue',
            'home_run': 'black'
        },

        category_orders={
            'events': ['single', 'double', 'triple', 'home_run']
        },

        hover_data={
            'game_date': True,
            'launch_speed': True,
            'launch_angle': True,
            'hc_x': False,
            'hc_y': False
        },
    )

    for trace in stadium_traces:
        fig.add_trace(trace)

    fig.update_layout(
        title=f"{firstName} {lastName} Spray Chart ({start} - {stop}, Stadium Displayed: {playerTeamTag})",
        showlegend=True,
        legend_title_text='Batted Ball Events:',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            title=None
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            title=None
        )
    )


    fig.show()


def main():
    data = getData(firstName, lastName, start, stop)
    print("Data scraped successfully.")
    print(f"Scraped data shape: {data.shape}")
    data = filterData(data)
    print("Data cleaned successfully.")
    print(f"Cleaned data shape: {data.shape}")
    plotStadium(data, playerTeam)
    plotStadiumInteractive(data, playerTeam)

if __name__ == "__main__":
    main()