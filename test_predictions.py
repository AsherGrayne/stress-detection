"""
Test predictions with different stress level data
"""
from predict import load_model, predict_single_point
from datetime import datetime

# Load model
print("Loading model...")
model = load_model('random_forest.joblib')

# Test cases based on training data patterns
test_cases = [
    {'X': -31, 'Y': 5, 'Z': 0, 'EDA': 0.3, 'HR': 81, 'TEMP': 29, 'name': 'Low Stress'},
    {'X': -26, 'Y': -8, 'Z': 0, 'EDA': 1.0, 'HR': 86, 'TEMP': 32.5, 'name': 'Medium Stress'},
    {'X': -37, 'Y': 5, 'Z': 0, 'EDA': 5.0, 'HR': 87, 'TEMP': 32, 'name': 'High Stress'},
]

print("\nTesting predictions:")
print("="*60)
for test in test_cases:
    pred, proba = predict_single_point(
        model=model,
        X=test['X'],
        Y=test['Y'],
        Z=test['Z'],
        EDA=test['EDA'],
        HR=test['HR'],
        TEMP=test['TEMP'],
        datetime_str=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    print(f"{test['name']:20s} -> Predicted: {pred:.0f} (Confidence: {max(proba):.2%})")
    print(f"  Probabilities: Class 0={proba[0]:.2%}, Class 1={proba[1]:.2%}, Class 2={proba[2]:.2%}")
print("="*60)

