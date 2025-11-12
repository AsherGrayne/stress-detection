import joblib
import pandas as pd

# Load model
model = joblib.load('models/random_forest.joblib')

print("Model type:", type(model))
print("\nModel attributes:")
for attr in dir(model):
    if not attr.startswith('_'):
        try:
            val = getattr(model, attr)
            if not callable(val):
                print(f"  {attr}: {type(val)}")
        except:
            pass

# Check if model has feature names
if hasattr(model, 'feature_names_in_'):
    print(f"\nExpected features ({len(model.feature_names_in_)}):")
    for i, name in enumerate(model.feature_names_in_):
        print(f"  {i}: {name}")

# Test with a sample
print("\n\nTesting prediction with sample data...")
try:
    test_data = {
        'X': [-21.0],
        'Y': [-53.0],
        'Z': [27.0],
        'EDA': [0.213944],
        'HR': [75.07],
        'TEMP': [30.37],
        'datetime': ['2020-05-08 22:11:34']
    }
    df = pd.DataFrame(test_data)
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
    
    print(f"\nDataFrame columns ({len(df.columns)}):")
    for i, col in enumerate(df.columns):
        print(f"  {i}: {col}")
    
    print(f"\nDataFrame shape: {df.shape}")
    print(f"\nDataFrame:\n{df}")
    
    # Try prediction
    pred = model.predict(df)
    print(f"\nPrediction successful: {pred[0]}")
    
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()

