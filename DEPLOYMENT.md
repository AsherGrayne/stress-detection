# Cloud Deployment Guide for ML Model API

This guide shows how to deploy your ML model to the cloud.

## Quick Start

### 1. Test Locally First

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API locally
python app.py
```

Test it:
```bash
python test_api.py
```

### 2. Deploy to Heroku

1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli

2. **Login to Heroku**:
```bash
heroku login
```

3. **Create Heroku App**:
```bash
heroku create your-app-name
```

4. **Set Environment Variables** (optional):
```bash
heroku config:set MODEL_NAME=random_forest.joblib
heroku config:set MODEL_DIR=models
```

5. **Deploy**:
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

6. **Your API will be at**: `https://your-app-name.herokuapp.com`

### 3. Deploy to Google Cloud Run

1. **Install Google Cloud SDK**

2. **Build and Deploy**:
```bash
gcloud run deploy ml-model-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 4. Deploy to AWS (Elastic Beanstalk)

1. **Install EB CLI**:
```bash
pip install awsebcli
```

2. **Initialize**:
```bash
eb init -p python-3.10 ml-model-api
```

3. **Create and Deploy**:
```bash
eb create ml-model-api-env
eb deploy
```

### 5. Deploy to Railway

1. **Install Railway CLI**:
```bash
npm i -g @railway/cli
```

2. **Login and Deploy**:
```bash
railway login
railway init
railway up
```

## API Endpoints

### POST `/predict`
Predict label from single sensor reading.

**Request:**
```json
{
  "X": -21.0,
  "Y": -53.0,
  "Z": 27.0,
  "EDA": 0.213944,
  "HR": 75.07,
  "TEMP": 30.37
}
```

**Response:**
```json
{
  "predicted_label": 1.0,
  "probabilities": {
    "class_0": 0.0,
    "class_1": 1.0,
    "class_2": 0.0
  },
  "confidence": 1.0
}
```

### POST `/predict/batch`
Predict labels for multiple sensor readings.

### GET `/health`
Check API health status.

### GET `/`
API information and available endpoints.

## Using from Raspberry Pi Pico W

Update your Pico W code to call the cloud API:

```python
import requests
import json

API_URL = "https://your-api.herokuapp.com/predict"

sensor_data = {
    "X": x_value,
    "Y": y_value,
    "Z": z_value,
    "EDA": eda_value,
    "HR": hr_value,
    "TEMP": temp_value
}

response = requests.post(API_URL, json=sensor_data)
result = response.json()
predicted_label = result['predicted_label']
```

## Environment Variables

- `MODEL_NAME`: Model file name (default: `random_forest.joblib`)
- `MODEL_DIR`: Models directory (default: `models`)
- `PORT`: Server port (default: `5000`)

## Notes

- Make sure your `models/` folder is included in deployment
- For production, set `debug=False` in `app.py`
- Consider adding authentication for production use
- Monitor API usage and set up logging

