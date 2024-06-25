#must run in anaconda base environment 

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
import matplotlib.pyplot as plt
#import warnings


path = "/Users/leofeingold/Desktop/pybaseball/stuff+_statcast_data2020-7-23To2024-06-1.csv"

df = pd.read_csv(path)

print(f"Starting Length: {len(df)}")

# mirror lefty x coordinates
condition = df["p_throws"] == "L"
df.loc[condition, 'release_pos_x'] = -1 * df.loc[condition, 'release_pos_x']
df.loc[condition, 'pfx_x'] = -1 * df.loc[condition, 'pfx_x']

# remove hit by pitch description
df = df[df["description"] != 'hit_by_pitch']

# select the columns I want
df = df[['release_speed', 'release_pos_x', 'release_pos_z', 'pfx_x', 'pfx_z', 'release_spin_rate', 'release_extension', 'spin_axis', 'mean_delta_run_exp']]

# remove NaN rows and drop na's
df = df.apply(pd.to_numeric, errors='coerce')
df = df.dropna()

# print length to make sure I still have data
print(f"After Some Drops, Length: {len(df)}")

# normalize each training parameter to have a mean of 0 and standard deviation of 1
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df.drop('mean_delta_run_exp', axis=1))
df_scaled = pd.DataFrame(scaled_features, columns=df.columns[:-1])
df_scaled['mean_delta_run_exp'] = df['mean_delta_run_exp']

# drop na again to be sure
df_scaled.dropna(inplace=True)
df_scaled = df_scaled.apply(pd.to_numeric, errors='coerce')
print(f"df_scaled length: {len(df_scaled)}")


# split data into training and testing data
X = df_scaled.drop('mean_delta_run_exp', axis=1)
y = df_scaled['mean_delta_run_exp']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"X_train Shape: {X_train.shape}")
print(f"y_train Shape: {y_train.shape}")

model = xgb.XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)


mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean squared error: {mse}")
print(f"R2 score: {r2}")

plt.scatter(y_test, y_pred)
plt.xlabel("Actual delta run value")
plt.ylabel("Predicted delta run value")
plt.title("Actual vs Predicted Delta Run Value")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.show()

importance = model.feature_importances_
features = X.columns

for i, v in enumerate(importance):
    print(f"{features[i]}: {v}")

# Plot feature importance
xgb.plot_importance(model)
plt.show()