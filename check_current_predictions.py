"""
Check what the current sensor data is predicting
"""
import json
import pandas as pd
from predict import load_model, predict_single_point
from datetime import datetime

# Load model
print("Loading model...")
model = load_model('random_forest.joblib')

# Load current sensor data
with open('sensor_data.json', 'r') as f:
    sensor_data = json.load(f)

if not sensor_data:
    print("No sensor data found!")
    exit()

print(f"\nChecking last 10 sensor readings:")
print("="*80)

# Check last 10 readings
for i, reading in enumerate(sensor_data[-10:], 1):
    pred, proba = predict_single_point(
        model=model,
        X=reading['X'],
        Y=reading['Y'],
        Z=reading['Z'],
        EDA=reading['EDA'],
        HR=reading['HR'],
        TEMP=reading['TEMP'],
        datetime_str=reading['timestamp']
    )
    
    print(f"{i}. EDA={reading['EDA']:.3f}, HR={reading['HR']:.1f}, TEMP={reading['TEMP']:.2f}")
    print(f"   Predicted: {pred:.0f} | Probs: 0={proba[0]:.1%}, 1={proba[1]:.1%}, 2={proba[2]:.1%}")
    print()

print("="*80)
print("\nSummary:")
pred_counts = {}
for reading in sensor_data[-20:]:  # Last 20
    pred, _ = predict_single_point(
        model=model,
        X=reading['X'],
        Y=reading['Y'],
        Z=reading['Z'],
        EDA=reading['EDA'],
        HR=reading['HR'],
        TEMP=reading['TEMP'],
        datetime_str=reading['timestamp']
    )
    pred_counts[pred] = pred_counts.get(pred, 0) + 1

for label, count in sorted(pred_counts.items()):
    print(f"  Label {label:.0f}: {count} predictions")

