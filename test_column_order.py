import joblib
import pandas as pd

# Load model
model = joblib.load('models/random_forest.joblib')

# Test exactly like predict.py does
X, Y, Z, EDA, HR, TEMP = -21.0, -53.0, 27.0, 0.213944, 75.07, 30.37
datetime_str = '2020-05-08 22:11:34'

# Create dataframe with single row (exactly like predict.py)
data = {
    'X': [X],
    'Y': [Y],
    'Z': [Z],
    'EDA': [EDA],
    'HR': [HR],
    'TEMP': [TEMP],
    'datetime': [datetime_str]
}

df = pd.DataFrame(data)

# Extract datetime features
df['datetime'] = pd.to_datetime(df['datetime'])
df['datetime_hour'] = df['datetime'].dt.hour
df['datetime_day'] = df['datetime'].dt.day
df['datetime_month'] = df['datetime'].dt.month
df['datetime_year'] = df['datetime'].dt.year
df['datetime_dow'] = df['datetime'].dt.dayofweek

# Drop non-feature columns
non_feature_cols = ['id', 'datetime', 'Unnamed: 0']
for col in non_feature_cols:
    if col in df.columns:
        df = df.drop(columns=[col])

print("Final DataFrame columns:")
print(df.columns.tolist())
print("\nModel expects:")
print(model.feature_names_in_.tolist())
print("\nColumns match:", list(df.columns) == list(model.feature_names_in_))
print("\nColumn order match:", df.columns.tolist() == model.feature_names_in_.tolist())

# Try prediction
try:
    pred = model.predict(df)[0]
    print(f"\nSUCCESS - Prediction: {pred}")
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

