from pybaseball import playerid_lookup
from pybaseball import statcast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dateInitial = '2024-05-26'
dateEnd = '2024-05-27'

def scrapeAndSaveData(start, end):
    data = statcast(start_dt = start, end_dt = end)
    return data

def main():
    data = scrapeAndSaveData(start=dateInitial, end=dateEnd)
    print(data.columns)

if __name__ == "__main__":
    main()