"""
Hugging Face Spaces API for ML Model Prediction
Deploy this to Hugging Face Spaces
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# Hugging Face Spaces automatically sets PORT
port = int(os.environ.get("PORT", 7860))

# Load model on startup
MODEL_NAME = os.getenv('MODEL_NAME', 'random_forest.joblib')
MODEL_DIR = os.getenv('MODEL_DIR', 'models')

print(f"Loading model: {MODEL_NAME}")
try:
    model_path = os.path.join(MODEL_DIR, MODEL_NAME)
    model = joblib.load(model_path)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# extract_datetime_features function removed - now handled in predict_single_point

def predict_single_point(model, X, Y, Z, EDA, HR, TEMP, datetime_str):
    """Make prediction for a single data point - ensures DataFrame is maintained"""
    # Parse datetime first
    dt = pd.to_datetime(datetime_str)
    
    # Get expected column order from model (ColumnTransformer uses column NAMES, not indices)
    if hasattr(model, 'feature_names_in_'):
        expected_columns = model.feature_names_in_.tolist()
    else:
        # Fallback: use the standard order
        expected_columns = ['X', 'Y', 'Z', 'EDA', 'HR', 'TEMP', 
                          'datetime_year', 'datetime_month', 'datetime_day', 
                          'datetime_hour', 'datetime_dow']
    
    # Create DataFrame with values in EXACT order expected by model
    # ColumnTransformer uses column NAMES (not indices), so it REQUIRES a DataFrame
    # Create as list of lists to ensure exact order and column assignment
    values = [
        float(X),
        float(Y),
        float(Z),
        float(EDA),
        float(HR),
        float(TEMP),
        int(dt.year),
        int(dt.month),
        int(dt.day),
        int(dt.hour),
        int(dt.dayofweek)
    ]
    
    # Create DataFrame with explicit column names - ColumnTransformer needs column names
    df = pd.DataFrame([values], columns=expected_columns)
    
    # Ensure DataFrame type and reset index to avoid any index issues
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Failed to create DataFrame, got {type(df)}")
    
    # Reset index to ensure clean DataFrame
    df = df.reset_index(drop=True)
    
    # Verify we have a DataFrame (not array) - ColumnTransformer will fail with array
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(df)}")
    
    # Verify columns match exactly (ColumnTransformer uses column names)
    if list(df.columns) != expected_columns:
        df = df[expected_columns]
        # Re-verify after reordering
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame(df, columns=expected_columns)
    
    # Ensure all columns are present
    missing_cols = set(expected_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing columns in DataFrame: {missing_cols}")
    
    # Make prediction - ColumnTransformer REQUIRES DataFrame with named columns
    # It was trained with column names, so it cannot accept numpy arrays
    prediction = model.predict(df)[0]
    
    # Get probabilities if available
    try:
        probabilities = model.predict_proba(df)[0]
    except:
        probabilities = None
    
    return prediction, probabilities

@app.route('/')
def home():
    """API home endpoint"""
    return jsonify({
        'message': 'ML Model Prediction API on Hugging Face',
        'status': 'running',
        'model': MODEL_NAME if model else 'not loaded',
        'endpoints': {
            '/predict': 'POST - Predict label from sensor data',
            '/health': 'GET - Check API health'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict label from sensor data
    
    Expected JSON body:
    {
        "X": -21.0,
        "Y": -53.0,
        "Z": 27.0,
        "EDA": 0.213944,
        "HR": 75.07,
        "TEMP": 30.37,
        "datetime": "2020-05-08 22:11:34"  // optional
    }
    """
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['X', 'Y', 'Z', 'EDA', 'HR', 'TEMP']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}'
            }), 400
        
        # Get datetime or use current time
        datetime_str = data.get('datetime', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Make prediction
        predicted_label, probabilities = predict_single_point(
            model=model,
            X=float(data['X']),
            Y=float(data['Y']),
            Z=float(data['Z']),
            EDA=float(data['EDA']),
            HR=float(data['HR']),
            TEMP=float(data['TEMP']),
            datetime_str=datetime_str
        )
        
        # Prepare response
        response = {
            'predicted_label': float(predicted_label),
            'input_data': {
                'X': data['X'],
                'Y': data['Y'],
                'Z': data['Z'],
                'EDA': data['EDA'],
                'HR': data['HR'],
                'TEMP': data['TEMP'],
                'datetime': datetime_str
            }
        }
        
        # Add probabilities if available
        if probabilities is not None:
            response['probabilities'] = {
                f'class_{i}': float(prob) for i, prob in enumerate(probabilities)
            }
            response['confidence'] = float(max(probabilities))
        
        return jsonify(response), 200
        
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        error_details = {
            'error': str(e),
            'error_type': type(e).__name__,
            'traceback': error_traceback
        }
        # Log full error for debugging
        print(f"Prediction error: {error_details}")
        print(f"Full traceback:\n{error_traceback}")
        
        # Provide hint for ColumnTransformer error
        if 'Specifying the columns using strings is only supported for dataframes' in str(e):
            error_details['hint'] = 'ColumnTransformer requires pandas DataFrame. Input may have been converted to numpy array.'
            error_details['solution'] = 'Ensure DataFrame is passed with correct column names matching model.feature_names_in_'
        
        return jsonify(error_details), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)

