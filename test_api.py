"""
Test script for the cloud API
Run this to test your deployed API or local server
"""
import requests
import json

# Change this to your API URL
API_URL = "http://localhost:5000"  # Local testing
# API_URL = "https://your-app.herokuapp.com"  # Heroku
# API_URL = "https://your-api.run.app"  # Google Cloud Run

def test_single_prediction():
    """Test single prediction endpoint"""
    print("Testing single prediction...")
    print("="*60)
    
    url = f"{API_URL}/predict"
    
    # Sample sensor data
    data = {
        "X": -21.0,
        "Y": -53.0,
        "Z": 27.0,
        "EDA": 0.213944,
        "HR": 75.07,
        "TEMP": 30.37,
        "datetime": "2020-05-08 22:11:34"
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}")
        print(f"\nPredicted Label: {result['predicted_label']}")
        if 'probabilities' in result:
            print(f"Confidence: {result['confidence']:.2%}")
        
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None

def test_batch_prediction():
    """Test batch prediction endpoint"""
    print("\n\nTesting batch prediction...")
    print("="*60)
    
    url = f"{API_URL}/predict/batch"
    
    data = {
        "data": [
            {
                "X": -21.0,
                "Y": -53.0,
                "Z": 27.0,
                "EDA": 0.213944,
                "HR": 75.07,
                "TEMP": 30.37
            },
            {
                "X": -49.0,
                "Y": -20.0,
                "Z": -37.0,
                "EDA": 0.237003,
                "HR": 75.78,
                "TEMP": 30.71
            }
        ]
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Total predictions: {result['count']}")
        print(f"\nResults:")
        for i, pred in enumerate(result['predictions']):
            if 'error' not in pred:
                print(f"  {i+1}. Label: {pred['predicted_label']}, "
                      f"Confidence: {pred.get('confidence', 0):.2%}")
            else:
                print(f"  {i+1}. Error: {pred['error']}")
        
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None

def test_health():
    """Test health endpoint"""
    print("\n\nTesting health check...")
    print("="*60)
    
    url = f"{API_URL}/health"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        print(f"Status: {result['status']}")
        print(f"Model loaded: {result['model_loaded']}")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("Testing Cloud ML API")
    print("="*60)
    print(f"API URL: {API_URL}\n")
    
    # Test health
    test_health()
    
    # Test single prediction
    test_single_prediction()
    
    # Test batch prediction
    test_batch_prediction()
    
    print("\n" + "="*60)
    print("Testing complete!")

