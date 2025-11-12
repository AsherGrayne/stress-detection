import joblib
import pandas as pd
import numpy as np

# Load model
model = joblib.load('models/random_forest.joblib')
prep = model.named_steps['prep']

print("=== ColumnTransformer Configuration ===")
print(f"Type: {type(prep)}")
print(f"\nTransformers:")
for i, (name, trans, cols) in enumerate(prep.transformers):
    print(f"  {i}. Name: {name}")
    print(f"     Transformer: {type(trans).__name__}")
    print(f"     Columns: {cols}")
    print(f"     Columns type: {type(cols)}")
    if isinstance(cols, list):
        print(f"     First element type: {type(cols[0])}")
        if cols:
            print(f"     First element: {cols[0]}")

print(f"\nRemainder: {prep.remainder}")
print(f"Sparse output: {prep.sparse_output_}")
if hasattr(prep, 'feature_names_in_'):
    print(f"Feature names in: {prep.feature_names_in_}")

# Test with DataFrame
print("\n=== Testing with DataFrame ===")
X, Y, Z, EDA, HR, TEMP = -21.0, -53.0, 27.0, 0.213944, 75.07, 30.37
dt = pd.to_datetime('2020-05-08 22:11:34')

expected_columns = model.feature_names_in_.tolist()
df = pd.DataFrame({
    'X': [X],
    'Y': [Y],
    'Z': [Z],
    'EDA': [EDA],
    'HR': [HR],
    'TEMP': [TEMP],
    'datetime_year': [dt.year],
    'datetime_month': [dt.month],
    'datetime_day': [dt.day],
    'datetime_hour': [dt.hour],
    'datetime_dow': [dt.dayofweek]
}, columns=expected_columns)

print(f"DataFrame columns: {df.columns.tolist()}")
print(f"DataFrame shape: {df.shape}")
print(f"DataFrame type: {type(df)}")

try:
    result_df = prep.transform(df)
    print(f"Transform with DataFrame: SUCCESS")
    print(f"  Output type: {type(result_df)}")
    print(f"  Output shape: {result_df.shape}")
except Exception as e:
    print(f"Transform with DataFrame: FAILED - {e}")

# Test with numpy array in correct order
print("\n=== Testing with NumPy Array (using indices) ===")
# Get the values in the exact order the model expects
array_data = df[expected_columns].values
print(f"Array shape: {array_data.shape}")
print(f"Array type: {type(array_data)}")

try:
    result_array = prep.transform(array_data)
    print(f"Transform with Array: SUCCESS")
    print(f"  Output type: {type(result_array)}")
    print(f"  Output shape: {result_array.shape}")
except Exception as e:
    print(f"Transform with Array: FAILED - {e}")
    import traceback
    traceback.print_exc()

# Try full pipeline with DataFrame
print("\n=== Testing Full Pipeline with DataFrame ===")
try:
    pred_df = model.predict(df)
    print(f"Pipeline predict with DataFrame: SUCCESS - {pred_df[0]}")
except Exception as e:
    print(f"Pipeline predict with DataFrame: FAILED - {e}")
    import traceback
    traceback.print_exc()

# Try full pipeline with array
print("\n=== Testing Full Pipeline with Array ===")
try:
    pred_array = model.predict(array_data)
    print(f"Pipeline predict with Array: SUCCESS - {pred_array[0]}")
except Exception as e:
    print(f"Pipeline predict with Array: FAILED - {e}")
    import traceback
    traceback.print_exc()

