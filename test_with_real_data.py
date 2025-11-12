"""
Test predictions with actual training data samples
"""
import pandas as pd
from predict import load_model, predict_single_point

# Load model
print("Loading model...")
model = load_model('random_forest.joblib')

# Load training data
df = pd.read_csv('balanced_data.csv')

# Get actual samples from each class
print("\nTesting with REAL training data samples:")
print("="*60)

# Low stress sample
low_sample = df[df['label'] == 0.0].iloc[0]
pred_low, proba_low = predict_single_point(
    model=model,
    X=low_sample['X'],
    Y=low_sample['Y'],
    Z=low_sample['Z'],
    EDA=low_sample['EDA'],
    HR=low_sample['HR'],
    TEMP=low_sample['TEMP'],
    datetime_str=low_sample['datetime']
)
print(f"Actual Label: 0.0 (Low)")
print(f"  X={low_sample['X']:.1f}, Y={low_sample['Y']:.1f}, Z={low_sample['Z']:.1f}")
print(f"  EDA={low_sample['EDA']:.3f}, HR={low_sample['HR']:.1f}, TEMP={low_sample['TEMP']:.2f}")
print(f"  Predicted: {pred_low:.0f} (Confidence: {max(proba_low):.2%})")
print(f"  Probabilities: 0={proba_low[0]:.2%}, 1={proba_low[1]:.2%}, 2={proba_low[2]:.2%}")
print()

# Medium stress sample
med_sample = df[df['label'] == 1.0].iloc[0]
pred_med, proba_med = predict_single_point(
    model=model,
    X=med_sample['X'],
    Y=med_sample['Y'],
    Z=med_sample['Z'],
    EDA=med_sample['EDA'],
    HR=med_sample['HR'],
    TEMP=med_sample['TEMP'],
    datetime_str=med_sample['datetime']
)
print(f"Actual Label: 1.0 (Medium)")
print(f"  X={med_sample['X']:.1f}, Y={med_sample['Y']:.1f}, Z={med_sample['Z']:.1f}")
print(f"  EDA={med_sample['EDA']:.3f}, HR={med_sample['HR']:.1f}, TEMP={med_sample['TEMP']:.2f}")
print(f"  Predicted: {pred_med:.0f} (Confidence: {max(proba_med):.2%})")
print(f"  Probabilities: 0={proba_med[0]:.2%}, 1={proba_med[1]:.2%}, 2={proba_med[2]:.2%}")
print()

# High stress sample
high_sample = df[df['label'] == 2.0].iloc[0]
pred_high, proba_high = predict_single_point(
    model=model,
    X=high_sample['X'],
    Y=high_sample['Y'],
    Z=high_sample['Z'],
    EDA=high_sample['EDA'],
    HR=high_sample['HR'],
    TEMP=high_sample['TEMP'],
    datetime_str=high_sample['datetime']
)
print(f"Actual Label: 2.0 (High)")
print(f"  X={high_sample['X']:.1f}, Y={high_sample['Y']:.1f}, Z={high_sample['Z']:.1f}")
print(f"  EDA={high_sample['EDA']:.3f}, HR={high_sample['HR']:.1f}, TEMP={high_sample['TEMP']:.2f}")
print(f"  Predicted: {pred_high:.0f} (Confidence: {max(proba_high):.2%})")
print(f"  Probabilities: 0={proba_high[0]:.2%}, 1={proba_high[1]:.2%}, 2={proba_high[2]:.2%}")
print("="*60)

