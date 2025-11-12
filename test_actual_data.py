"""
Test with actual data from balanced_data.csv to verify predictions match labels
"""
import pandas as pd
from predict import load_model, predict_single_point

# Load model
print("Loading model...")
model = load_model('random_forest.joblib')

# Load training data
df = pd.read_csv('balanced_data.csv')

# Test with samples from each class
print("\nTesting predictions with actual training data:")
print("="*80)

correct = 0
total = 0

for label in [0.0, 1.0, 2.0]:
    samples = df[df['label'] == label].sample(min(5, len(df[df['label'] == label])))
    print(f"\nLabel {label:.0f} samples:")
    for idx, row in samples.iterrows():
        pred, proba = predict_single_point(
            model=model,
            X=row['X'],
            Y=row['Y'],
            Z=row['Z'],
            EDA=row['EDA'],
            HR=row['HR'],
            TEMP=row['TEMP'],
            datetime_str=row['datetime']
        )
        match = "OK" if pred == label else "X"
        total += 1
        if pred == label:
            correct += 1
        print(f"  {match} EDA={row['EDA']:.3f}, HR={row['HR']:.1f}, TEMP={row['TEMP']:.2f} -> Pred: {pred:.0f} (Conf: {max(proba):.1%})")

print("\n" + "="*80)
print(f"Accuracy: {correct}/{total} = {correct/total:.1%}")

