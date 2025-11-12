import joblib
import pandas as pd
import numpy as np

# Load model
model = joblib.load('models/random_forest.joblib')

# Simulate the prediction
X, Y, Z, EDA, HR, TEMP = -21.0, -53.0, 27.0, 0.213944, 75.07, 30.37
datetime_str = '2020-05-08 22:11:34'

# Create dataframe
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
print(f"1. Initial DataFrame type: {type(df)}")
print(f"   Is DataFrame: {isinstance(df, pd.DataFrame)}")

# Extract datetime features
df['datetime'] = pd.to_datetime(df['datetime'])
df['datetime_hour'] = df['datetime'].dt.hour
df['datetime_day'] = df['datetime'].dt.day
df['datetime_month'] = df['datetime'].dt.month
df['datetime_year'] = df['datetime'].dt.year
df['datetime_dow'] = df['datetime'].dt.dayofweek

print(f"2. After datetime extraction type: {type(df)}")
print(f"   Is DataFrame: {isinstance(df, pd.DataFrame)}")

# Drop non-feature columns
non_feature_cols = ['id', 'datetime', 'Unnamed: 0']
for col in non_feature_cols:
    if col in df.columns:
        df = df.drop(columns=[col])

print(f"3. After dropping columns type: {type(df)}")
print(f"   Is DataFrame: {isinstance(df, pd.DataFrame)}")
print(f"   Columns: {df.columns.tolist()}")

# Reorder columns
if hasattr(model, 'feature_names_in_'):
    expected_order = model.feature_names_in_.tolist()
    if set(df.columns) == set(expected_order):
        df = df[expected_order]
        print(f"4. After reordering type: {type(df)}")
        print(f"   Is DataFrame: {isinstance(df, pd.DataFrame)}")
        print(f"   Columns: {df.columns.tolist()}")

# Ensure it's a DataFrame (not array)
if not isinstance(df, pd.DataFrame):
    print("WARNING: df is not a DataFrame, converting...")
    df = pd.DataFrame(df, columns=expected_order)
else:
    print(f"5. Final type: {type(df)}")
    print(f"   Is DataFrame: {isinstance(df, pd.DataFrame)}")
    print(f"   DataFrame dtypes:\n{df.dtypes}")

# Test prediction
print("\nTesting prediction...")
try:
    # Check what the ColumnTransformer receives
    prep = model.named_steps['prep']
    print(f"ColumnTransformer type: {type(prep)}")
    print(f"Input to ColumnTransformer type: {type(df)}")
    print(f"Input is DataFrame: {isinstance(df, pd.DataFrame)}")
    
    pred = model.predict(df)
    print(f"SUCCESS - Prediction: {pred[0]}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

