"""
Example: Call your cloud ML API from anywhere
"""
import requests
import json

# Your cloud API URL (update this after deployment)
API_URL = "http://localhost:5000"  # Local
# API_URL = "https://your-app.herokuapp.com"  # Heroku
# API_URL = "https://your-api.run.app"  # Google Cloud

def predict_from_cloud(sensor_data):
    """
    Send sensor data to cloud API and get prediction
    
    Parameters:
    - sensor_data: dict with X, Y, Z, EDA, HR, TEMP
    """
    url = f"{API_URL}/predict"
    
    try:
        response = requests.post(url, json=sensor_data, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Sample sensor reading
    sensor_data = {
        "X": -21.0,
        "Y": -53.0,
        "Z": 27.0,
        "EDA": 0.213944,
        "HR": 75.07,
        "TEMP": 30.37
    }
    
    print("Sending sensor data to cloud API...")
    print(f"Data: {sensor_data}\n")
    
    result = predict_from_cloud(sensor_data)
    
    if result:
        print("Prediction Result:")
        print(f"  Predicted Label: {result['predicted_label']}")
        if 'probabilities' in result:
            print(f"  Confidence: {result['confidence']:.2%}")
            print(f"  Probabilities: {result['probabilities']}")
    else:
        print("Failed to get prediction")

