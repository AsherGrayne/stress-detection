"""
Cloud API for ML Model Prediction
Deploy this to cloud platforms (Heroku, AWS, Google Cloud, etc.)
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from predict import load_model, predict_single_point

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Load model on startup
MODEL_NAME = os.getenv('MODEL_NAME', 'random_forest.joblib')
MODEL_DIR = os.getenv('MODEL_DIR', 'models')

print(f"Loading model: {MODEL_NAME}")
try:
    model = load_model(MODEL_NAME, model_dir=MODEL_DIR)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/')
def home():
    """API home endpoint"""
    return jsonify({
        'message': 'ML Model Prediction API',
        'status': 'running',
        'model': MODEL_NAME if model else 'not loaded',
        'endpoints': {
            '/predict': 'POST - Predict label from sensor data',
            '/health': 'GET - Check API health',
            '/models': 'GET - List available models'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

@app.route('/models', methods=['GET'])
def list_models():
    """List available models"""
    import os
    models_dir = MODEL_DIR
    if os.path.exists(models_dir):
        models = [f for f in os.listdir(models_dir) if f.endswith('.joblib')]
        return jsonify({'models': models})
    return jsonify({'models': []})

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
        "datetime": "2020-05-08 22:11:34"  // optional, defaults to current time
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
            datetime_str=datetime_str,
            id_val=data.get('id', None)
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
        return jsonify({'error': str(e)}), 500

@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    """
    Predict labels for multiple data points
    
    Expected JSON body:
    {
        "data": [
            {"X": -21.0, "Y": -53.0, "Z": 27.0, "EDA": 0.213, "HR": 75.07, "TEMP": 30.37},
            {"X": -49.0, "Y": -20.0, "Z": -37.0, "EDA": 0.237, "HR": 75.78, "TEMP": 30.71}
        ]
    }
    """
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        if 'data' not in data or not isinstance(data['data'], list):
            return jsonify({'error': 'Expected "data" field with list of sensor readings'}), 400
        
        predictions = []
        for item in data['data']:
            required_fields = ['X', 'Y', 'Z', 'EDA', 'HR', 'TEMP']
            missing = [f for f in required_fields if f not in item]
            
            if missing:
                predictions.append({
                    'error': f'Missing fields: {missing}',
                    'input': item
                })
                continue
            
            datetime_str = item.get('datetime', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            predicted_label, probabilities = predict_single_point(
                model=model,
                X=float(item['X']),
                Y=float(item['Y']),
                Z=float(item['Z']),
                EDA=float(item['EDA']),
                HR=float(item['HR']),
                TEMP=float(item['TEMP']),
                datetime_str=datetime_str
            )
            
            result = {
                'predicted_label': float(predicted_label),
                'input_data': item
            }
            
            if probabilities is not None:
                result['probabilities'] = {
                    f'class_{i}': float(prob) for i, prob in enumerate(probabilities)
                }
                result['confidence'] = float(max(probabilities))
            
            predictions.append(result)
        
        return jsonify({
            'predictions': predictions,
            'count': len(predictions)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

