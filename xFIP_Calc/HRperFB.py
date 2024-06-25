import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from pybaseball import statcast
import pandas as pd


seasons = [("2024-01-01", "2024-06-25"), ("2023-01-01", "2023-12-31"), ("2022-01-01", "2022-12-31"), ("2021-01-01", "2021-12-31")]
league_avg_hr_fb_rates = {}


for start, end in seasons:
    print(f"Processing season {start[:4]}...")
    print("\n\n")
    league_data = statcast(start, end)
    print("\n\n")

    print("\n\n")
    league_data = league_data[league_data['game_type'] == "R"]
    print("\n\n")
    
    total_home_runs = league_data['events'].value_counts().get('home_run', 0)
    total_fly_balls_1 = league_data['bb_type'].value_counts().get('fly_ball', 0)
    fly_balls = league_data[(league_data['la'] >= 25) & (league_data['la'] <= 50)]
    total_fly_balls = len(fly_balls)

    league_avg_hr_fb = total_home_runs / total_fly_balls if total_fly_balls > 0 else float('nan')
    league_avg_hr_fb_rates[f"{start[:4]}"] = league_avg_hr_fb
    print("\n\n")
    print(f"{start[:4]}:\nFB: {total_fly_balls}\nHR: {total_home_runs}")

for season, hr_fb_rate in league_avg_hr_fb_rates.items():
    print(f"League HR/FB rate for {season}: {hr_fb_rate}")
    '''
    using: total_fly_balls_1
    League HR/FB rate for 2024: 0.1572066126092149
    League HR/FB rate for 2023: 0.18059274305234974
    League HR/FB rate for 2022: 0.1633618394261191
    League HR/FB rate for 2021: 0.1905433563071005
    '''