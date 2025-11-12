import os
import pandas as pd
from predict import load_model, predict_single_point

# Get all model files from models directory
models_dir = "models"
model_files = [f for f in os.listdir(models_dir) if f.endswith('.joblib')]
model_files.sort()

# Load test data (balanced_data.csv)
print("Loading test data...")
df = pd.read_csv("balanced_data.csv")

# Take the first row as an example
row = df.iloc[0]
print(f"\n{'='*60}")
print(f"Test data point:")
print(f"{'='*60}")
print(f"X: {row['X']}, Y: {row['Y']}, Z: {row['Z']}")
print(f"EDA: {row['EDA']}, HR: {row['HR']}, TEMP: {row['TEMP']}")
print(f"Datetime: {row['datetime']}")
print(f"Actual label: {row['label']}")
print(f"{'='*60}\n")

# Predict with all models
results = []
for model_file in model_files:
    model_name = model_file.replace('.joblib', '')
    try:
        print(f"Loading {model_name} model...")
        model = load_model(model_file, model_dir=models_dir)
        
        # Predict for this single point
        predicted_label, probabilities = predict_single_point(
            model=model,
            X=row['X'],
            Y=row['Y'],
            Z=row['Z'],
            EDA=row['EDA'],
            HR=row['HR'],
            TEMP=row['TEMP'],
            datetime_str=row['datetime'],
            id_val=row.get('id', None)
        )
        
        results.append({
            'model': model_name,
            'predicted_label': predicted_label,
            'probabilities': probabilities,
            'correct': predicted_label == row['label']
        })
        
        print(f"\n{model_name.upper().replace('_', ' ')} Results:")
        print(f"  Predicted label: {predicted_label}")
        print(f"  Actual label: {row['label']}")
        print(f"  Correct: {'Yes' if predicted_label == row['label'] else 'No'}")
        
        if probabilities is not None:
            print(f"  Class probabilities:")
            for i, prob in enumerate(probabilities):
                print(f"    Class {i}: {prob:.4f}")
        print(f"{'-'*60}\n")
    except Exception as e:
        print(f"  ERROR: Failed to load or use {model_name} model")
        print(f"  Error: {str(e)}")
        print(f"{'-'*60}\n")
        results.append({
            'model': model_name,
            'predicted_label': None,
            'probabilities': None,
            'correct': False,
            'error': str(e)
        })

# Summary
print(f"\n{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
print(f"Actual label: {row['label']}")
print(f"\nPredictions by model:")
for result in results:
    if 'error' in result:
        print(f"  {result['model']:25s}: ERROR - {result['error'][:40]}")
    else:
        status = "CORRECT" if result['correct'] else "INCORRECT"
        pred_label = result['predicted_label'] if result['predicted_label'] is not None else "N/A"
        print(f"  {result['model']:25s}: {pred_label} ({status})")

correct_count = sum(1 for r in results if r['correct'])
print(f"\nCorrect predictions: {correct_count}/{len(results)}")
print(f"{'='*60}")

