from pybaseball import playerid_lookup, statcast_pitcher
import pandas as pd

# Player information
player_first_name = "Shane"
player_last_name = "McClanahan"
season_start = "2023-04-01"
season_end = "2023-10-01"

# Lookup player ID
player_id_df = playerid_lookup(player_last_name, player_first_name)
if player_id_df.empty:
    raise ValueError("Player not found.")
player_id = player_id_df['key_mlbam'].values[0]

# Fetch player data for the season
player_data = statcast_pitcher(season_start, season_end, player_id)

# Filter for regular season games
player_data = player_data[player_data['game_type'] == "R"]

# Calculate outs
outs_events = {
    'strikeout': 1,
    'field_out': 1,
    'force_out': 1,
    'grounded_into_double_play': 2,
    'double_play': 2,
    'caught_stealing_2b': 1,
}

total_outs = sum(player_data['events'].apply(lambda event: outs_events.get(event, 0)))

# Calculate total innings pitched
innings_pitched = total_outs / 3
print(f"Total innings pitched: {innings_pitched:.1f}")

# Calculate innings pitched to left-handed and right-handed batters
lefty_data = player_data[player_data['stand'] == 'L']
righty_data = player_data[player_data['stand'] == 'R']

total_lefty_outs = sum(lefty_data['events'].apply(lambda event: outs_events.get(event, 0)))
total_righty_outs = sum(righty_data['events'].apply(lambda event: outs_events.get(event, 0)))

lefty_innings_pitched = total_lefty_outs / 3
righty_innings_pitched = total_righty_outs / 3

print(f"Innings pitched to left-handed batters: {lefty_innings_pitched:.1f}")
print(f"Innings pitched to right-handed batters: {righty_innings_pitched:.1f}")
