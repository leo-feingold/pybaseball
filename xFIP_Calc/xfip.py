from pybaseball import playerid_lookup, statcast_pitcher, statcast
from pybaseball import pitching_stats
import pandas as pd
import warnings
warnings.simplefilter(action='ignore')

player_first_name = "Shane"
player_last_name = "McClanahan"
season = 2023
season_start = "2023-04-01"
season_end = "2023-10-01"

def calc_fip_constant_and_hr_fb(path, start, end):
    fip_const_df = pd.read_csv(path)
    league_fip_constant = fip_const_df[fip_const_df["Season"] == season]["cFIP"].values[0]

    #Retrieve league-wide data for the specified season
    league_data = statcast(start, end)
    league_data = league_data[league_data['game_type'] == "R"]

    # Calculate league HR/FB rate
    total_home_runs = league_data['events'].value_counts().get('home_run', 0)
    total_fly_balls = league_data['bb_type'].value_counts().get('fly_ball', 0)
    league_avg_hr_fb = total_home_runs / total_fly_balls if total_fly_balls > 0 else float('nan')

    return league_fip_constant, league_avg_hr_fb


# Function to calculate xFIP
def calculate_xfip(df, league_avg_hr_fb, league_fip_constant):
    df = df[df['game_type'] == "R"]

    # Calculate outs
    outs_events = {
        'strikeout': 1,
        'field_out': 1,
        'force_out': 1,
        'grounded_into_double_play': 2,
        'double_play': 2,
        'caught_stealing_2b': 1,
    }

    total_outs = sum(df['events'].apply(lambda event: outs_events.get(event, 0)))

    # Calculate total innings pitched
    innings_pitched = total_outs / 3
    print(f"Innings pitched: {innings_pitched:.1f}")

    # Calculate individual components
    strikeouts = df['events'].value_counts().get('strikeout', 0)
    walks = df['events'].value_counts().get('walk', 0) + df['events'].value_counts().get('hit_by_pitch', 0)
    fly_balls = df['bb_type'].value_counts().get('fly_ball', 0)
    print(df.columns)

    # Calculate xFIP
    if innings_pitched > 0:
        #((Fly balls / league average rate of HR per fly ball x 13) + (3 x (BB + HBP)) - (2 x K)) / IP + FIP constant
        xfip = ((fly_balls / (league_avg_hr_fb * 13)) + (3 * walks) - (2 * strikeouts)) / innings_pitched + league_fip_constant
    else:
        xfip = float('nan')
    
    return xfip

def main():
    path = "/Users/leofeingold/Desktop/pybaseball/FIPConstant.csv"
    league_fip_constant, league_avg_hr_fb = calc_fip_constant_and_hr_fb(path, season_start, season_end)

    # Look up the player's ID
    player_id_df = playerid_lookup(player_last_name, player_first_name)
    player_id = player_id_df['key_mlbam'].values[0]

    # Retrieve pitch-by-pitch data for the player
    player_data = statcast_pitcher(season_start, season_end, player_id)

    # Filter data for left-handed and right-handed batters
    lefty_data = player_data[player_data['stand'] == 'L']
    righty_data = player_data[player_data['stand'] == 'R']

    # Calculate xFIP for left-handed and right-handed batters
    lefty_xfip = calculate_xfip(lefty_data, league_avg_hr_fb, league_fip_constant)
    righty_xfip = calculate_xfip(righty_data, league_avg_hr_fb, league_fip_constant)

    # Print the results
    print(f"League Average HR/FB: {league_avg_hr_fb}")
    print(f"FIP Constant: {league_fip_constant}")
    print(f"{player_first_name} {player_last_name}'s xFIP vs Left-handed Batters in 2023: {lefty_xfip:.2f}")
    print(f"{player_first_name} {player_last_name}'s xFIP vs Right-handed Batters in 2023: {righty_xfip:.2f}")

if __name__ == "__main__":
    main()
