import joblib
import pandas as pd
import numpy as np
import argparse
import os

def load_model(model_name, model_dir="models"):
    """
    Loads a joblib model stored in the given directory.
    """
    path = os.path.join(model_dir, model_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found: {path}")
    return joblib.load(path)


def predict_single_point(model, X, Y, Z, EDA, HR, TEMP, datetime_str, id_val=None):
    """
    Predicts label for a single data point.
    
    Parameters:
    - model: Loaded joblib model
    - X, Y, Z: Accelerometer values
    - EDA: Electrodermal activity
    - HR: Heart rate
    - TEMP: Temperature
    - datetime_str: Datetime string (e.g., '2020-07-08 14:03:00')
    - id_val: Optional ID value
    
    Returns:
    - predicted_label: The predicted label
    - probabilities: Class probabilities (if available)
    """
    # Create dataframe with single row
    data = {
        'X': [X],
        'Y': [Y],
        'Z': [Z],
        'EDA': [EDA],
        'HR': [HR],
        'TEMP': [TEMP],
        'datetime': [datetime_str]
    }
    if id_val is not None:
        data['id'] = [id_val]
    
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
    
    # Predict
    pred = model.predict(df)[0]
    proba = None
    
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(df)[0]
    
    return pred, proba


def predict_from_csv(model, csv_file, target_column="label"):
    """
    Loads CSV, drops target if present, extracts datetime features, runs prediction.
    Returns original dataframe, predictions, and probabilities.
    """
    df = pd.read_csv(csv_file)
    original_df = df.copy()

    # If target is present, drop for prediction
    if target_column in df.columns:
        df_features = df.drop(columns=[target_column])
    else:
        df_features = df.copy()

    # Extract datetime features if datetime column exists
    if 'datetime' in df_features.columns:
        df_features['datetime'] = pd.to_datetime(df_features['datetime'])
        df_features['datetime_hour'] = df_features['datetime'].dt.hour
        df_features['datetime_day'] = df_features['datetime'].dt.day
        df_features['datetime_month'] = df_features['datetime'].dt.month
        df_features['datetime_year'] = df_features['datetime'].dt.year
        df_features['datetime_dow'] = df_features['datetime'].dt.dayofweek

    # Drop non-feature columns if they exist (but keep datetime features we just created)
    non_feature_cols = ['id', 'datetime', 'Unnamed: 0']
    for col in non_feature_cols:
        if col in df_features.columns:
            df_features = df_features.drop(columns=[col])

    preds = model.predict(df_features)
    probas = None

    # If the model supports predict_proba
    if hasattr(model, "predict_proba"):
        probas = model.predict_proba(df_features)

    return original_df, preds, probas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", type=str, required=True,
                    help="Name of the saved joblib model (e.g., random_forest.joblib)")
    ap.add_argument("--csv", type=str, required=True,
                    help="Path to CSV file containing data for prediction")
    ap.add_argument("--model_dir", type=str, default="models",
                    help="Directory where joblib models are stored")
    ap.add_argument("--output", type=str, default=None,
                    help="Output CSV file path to save predictions (default: input_file_predictions.csv)")
    args = ap.parse_args()

    # Load model
    print(f"Loading model: {args.model}")
    model = load_model(args.model, model_dir=args.model_dir)

    # Predict
    print(f"Reading input data: {args.csv}")
    original_df, preds, probas = predict_from_csv(model, args.csv)

    # Create output dataframe with predictions
    output_df = original_df.copy()
    output_df['predicted_label'] = preds

    # Add probabilities if available
    if probas is not None:
        proba_df = pd.DataFrame(probas, 
                               columns=[f'prob_class_{i}' for i in range(probas.shape[1])])
        output_df = pd.concat([output_df, proba_df], axis=1)

    # Determine output file path
    if args.output is None:
        base_name = os.path.splitext(args.csv)[0]
        output_path = f"{base_name}_predictions.csv"
    else:
        output_path = args.output

    # Save predictions
    output_df.to_csv(output_path, index=False)
    print(f"\nPredictions saved to: {output_path}")
    print(f"Total predictions: {len(preds)}")
    print(f"\nPrediction summary:")
    print(output_df['predicted_label'].value_counts().sort_index())

    if probas is not None:
        print(f"\nProbability columns added: {probas.shape[1]} classes")


if __name__ == "__main__":
    main()
