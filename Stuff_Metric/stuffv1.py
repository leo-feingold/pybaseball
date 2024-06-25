from pybaseball import statcast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import warnings

dateInitial = '2023-06-25'
dateEnd = '2023-06-27'

def scrapeData(start, end):
    warnings.simplefilter(action='ignore', category=FutureWarning)

    data = statcast(start_dt = start, end_dt = end)
    return data

def cleanData(df): 
    df.set_index('pitch_type', inplace=True)
    df = df[['release_speed', 'release_pos_x', 
        'release_pos_z','pfx_x', 
        'pfx_z', 'release_spin_rate', 'release_extension',
        'spin_axis', 'estimated_ba_using_speedangle']] 
    # 'vx0','vy0', 'vz0', 'ax', 'ay', 'az', 'plate_x', 'plate_z', game_date, player_name, pitcher, 
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna()
    return df

def splitData(df):
    X = df.drop('estimated_ba_using_speedangle', axis=1)
    y = df['estimated_ba_using_speedangle']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def trainModel(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def visualizeData(X_train, y_test, y_pred):
    r2 = r2_score(y_test, y_pred)
    numSamples = X_train.shape[0]
    plt.scatter(y_test, y_pred)
    plt.xlabel("Actual xwOBA")
    plt.ylabel("Predicted xwOBA")
    plt.title(f"Stuff+ Model: r^2 = {r2}, ({numSamples} Samples)")
    plt.show()

def main():
    data = scrapeData(start=dateInitial, end=dateEnd)
    print(data.columns)

    '''
    print("Data scraped successfully.")
    print(f"Scraped data shape: {data.shape}")
    data = cleanData(data)
    print("Data cleaned successfully.")
    print(f"Cleaned data shape: {data.shape}")
    X_train, X_test, y_train, y_test = splitData(data)
    print("Data split successfully.")
    model = trainModel(X_train, y_train)
    print("Model trained successfully")
    y_pred = model.predict(X_test)
    print("Prediction completed successfully.")
    visualizeData(X_train, y_test, y_pred)
    '''

if __name__ == "__main__":
    main()