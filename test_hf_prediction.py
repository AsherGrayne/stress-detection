import joblib
import pandas as pd
from datetime import datetime

# Load model
model = joblib.load('models/random_forest.joblib')

# Simulate the exact API request
X, Y, Z, EDA, HR, TEMP = -21.0, -53.0, 27.0, 0.213944, 75.07, 30.37
datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print("Testing prediction with API-like data...")
print(f"Input: X={X}, Y={Y}, Z={Z}, EDA={EDA}, HR={HR}, TEMP={TEMP}, datetime={datetime_str}")

# Create dataframe exactly like huggingface_deploy.py
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
print(f"\nInitial DataFrame columns: {df.columns.tolist()}")

# Extract datetime features
df['datetime'] = pd.to_datetime(df['datetime'])
df['datetime_hour'] = df['datetime'].dt.hour
df['datetime_day'] = df['datetime'].dt.day
df['datetime_month'] = df['datetime'].dt.month
df['datetime_year'] = df['datetime'].dt.year
df['datetime_dow'] = df['datetime'].dt.dayofweek

print(f"After datetime extraction: {df.columns.tolist()}")

# Drop non-feature columns
non_feature_cols = ['id', 'datetime', 'Unnamed: 0']
for col in non_feature_cols:
    if col in df.columns:
        df = df.drop(columns=[col])

print(f"After dropping columns: {df.columns.tolist()}")
print(f"Model expects: {model.feature_names_in_.tolist()}")

# Check if all required columns are present
missing_cols = set(model.feature_names_in_) - set(df.columns)
if missing_cols:
    print(f"\nWARNING: Missing columns: {missing_cols}")

extra_cols = set(df.columns) - set(model.feature_names_in_)
if extra_cols:
    print(f"WARNING: Extra columns: {extra_cols}")

# Try prediction
print("\nAttempting prediction...")
try:
    # Check DataFrame type
    print(f"DataFrame type: {type(df)}")
    print(f"DataFrame dtypes:\n{df.dtypes}")
    
    # Try to get the ColumnTransformer
    prep = model.named_steps['prep']
    print(f"\nColumnTransformer type: {type(prep)}")
    print(f"ColumnTransformer transformers: {prep.transformers}")
    
    # Try transform manually to see what happens
    print("\nTrying ColumnTransformer.transform() manually...")
    try:
        transformed = prep.transform(df)
        print(f"Transform successful! Output shape: {transformed.shape}")
    except Exception as e:
        print(f"Transform failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Try full pipeline predict
    print("\nTrying full pipeline predict...")
    pred = model.predict(df)
    print(f"SUCCESS - Prediction: {pred[0]}")
    
    # Try predict_proba
    proba = model.predict_proba(df)
    print(f"Probabilities: {proba[0]}")
    
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

