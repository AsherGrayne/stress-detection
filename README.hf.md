---
title: Stress Prediction API
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Stress Prediction API

ML model API for predicting stress levels from sensor data (EDA, HR, TEMP, Accelerometer).

## API Endpoints

### `GET /`
Get API information and available endpoints.

### `GET /health`
Health check endpoint.

### `POST /predict`
Predict stress level from sensor readings.

**Request:**
```json
{
  "X": -21.0,
  "Y": -53.0,
  "Z": 27.0,
  "EDA": 0.213944,
  "HR": 75.07,
  "TEMP": 30.37,
  "datetime": "2020-05-08 22:11:34"
}
```

**Response:**
```json
{
  "predicted_label": 1.0,
  "confidence": 0.95,
  "probabilities": {
    "class_0": 0.0,
    "class_1": 0.95,
    "class_2": 0.05
  },
  "input_data": {
    "X": -21.0,
    "Y": -53.0,
    "Z": 27.0,
    "EDA": 0.213944,
    "HR": 75.07,
    "TEMP": 30.37,
    "datetime": "2020-05-08 22:11:34"
  }
}
```

## Stress Levels

- **0**: Low stress
- **1**: Medium stress  
- **2**: High stress

## Usage Example

```python
import requests

url = "https://YOUR-USERNAME-YOUR-SPACE-NAME.hf.space/predict"

data = {
    "X": -21.0,
    "Y": -53.0,
    "Z": 27.0,
    "EDA": 0.213944,
    "HR": 75.07,
    "TEMP": 30.37
}

response = requests.post(url, json=data)
result = response.json()
print(f"Predicted stress level: {result['predicted_label']}")
print(f"Confidence: {result['confidence']:.2%}")
```

