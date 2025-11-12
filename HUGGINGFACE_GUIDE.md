# Hugging Face Spaces Deployment Guide

This guide shows how to deploy your ML model to Hugging Face Spaces for free API hosting.

## What is Hugging Face Spaces?

Hugging Face Spaces is a free platform to host ML models and create demos. It's perfect for:
- ✅ Hosting joblib models
- ✅ Creating REST APIs
- ✅ Free hosting (with GPU options available)
- ✅ Automatic HTTPS
- ✅ Public or private spaces

## Step-by-Step Deployment

### 1. Create Hugging Face Account

1. Go to [huggingface.co](https://huggingface.co)
2. Sign up for a free account
3. Verify your email

### 2. Create a New Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Fill in:
   - **Space name**: `stress-prediction-api` (or your choice)
   - **SDK**: Select **"Gradio"** or **"Docker"** (we'll use Docker)
   - **Visibility**: Public or Private
4. Click **"Create Space"**

### 3. Prepare Your Files

You need these files in your Space:

#### `app.py` (or use `huggingface_deploy.py`)
The Flask API code (already created for you)

#### `requirements.txt`
```
flask==2.3.0
flask-cors==4.0.0
scikit-learn==1.3.0
joblib==1.3.2
pandas==2.0.3
numpy==1.24.3
```

#### `Dockerfile`
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY models/ ./models/

# Expose port (Hugging Face uses 7860)
EXPOSE 7860

# Run the application
CMD python app.py
```

#### `README.md`
```markdown
---
title: Stress Prediction API
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Stress Prediction API

ML model API for predicting stress levels from sensor data.

## API Endpoints

### POST `/predict`
Predict stress level from sensor readings.

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
  "confidence": 0.95,
  "probabilities": {
    "class_0": 0.0,
    "class_1": 0.95,
    "class_2": 0.05
  }
}
```
```

### 4. Upload Files to Space

**Option A: Using Git (Recommended)**

1. Clone your Space repository:
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME
```

2. Copy your files:
```bash
# Copy the Flask app
cp huggingface_deploy.py app.py

# Copy models directory
cp -r models/ .

# Copy requirements.txt
# (create it with the content above)

# Copy Dockerfile
# (create it with the content above)
```

3. Commit and push:
```bash
git add .
git commit -m "Add ML model API"
git push
```

**Option B: Using Web Interface**

1. Go to your Space page
2. Click **"Files and versions"** tab
3. Click **"Add file"** → **"Upload files"**
4. Upload:
   - `app.py` (or `huggingface_deploy.py`)
   - `requirements.txt`
   - `Dockerfile`
   - `models/` folder (upload all `.joblib` files)

### 5. Wait for Deployment

- Hugging Face will automatically build and deploy your Space
- This takes 2-5 minutes
- You'll see build logs in the Space page
- When ready, you'll see "Running" status

## Using Your API

Once deployed, your API will be available at:
```
https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space
```

### Test the API

**Using curl:**
```bash
curl -X POST https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/predict \
  -H "Content-Type: application/json" \
  -d '{
    "X": -21.0,
    "Y": -53.0,
    "Z": 27.0,
    "EDA": 0.213944,
    "HR": 75.07,
    "TEMP": 30.37
  }'
```

**Using Python:**
```python
import requests

url = "https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/predict"

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
print(result)
```

**Using JavaScript:**
```javascript
fetch('https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    X: -21.0,
    Y: -53.0,
    Z: 27.0,
    EDA: 0.213944,
    HR: 75.07,
    TEMP: 30.37
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## API Endpoints

### `GET /`
Get API information

### `GET /health`
Health check endpoint

### `POST /predict`
Predict stress level from sensor data

**Request Body:**
```json
{
  "X": -21.0,
  "Y": -53.0,
  "Z": 27.0,
  "EDA": 0.213944,
  "HR": 75.07,
  "TEMP": 30.37,
  "datetime": "2020-05-08 22:11:34"  // optional
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

## Updating Your Model

1. Make changes to your code
2. Commit and push to the Space repository
3. Hugging Face will automatically rebuild and redeploy

## Tips

1. **File Size Limits**: Free tier has limits. If models are large, consider:
   - Using Git LFS for large files
   - Compressing models
   - Using model quantization

2. **Multiple Models**: You can load multiple models and create endpoints for each:
   ```python
   models = {
       'random_forest': joblib.load('models/random_forest.joblib'),
       'logistic_regression': joblib.load('models/logistic_regression.joblib')
   }
   ```

3. **Environment Variables**: Set secrets in Space settings:
   - Go to Space → Settings → Secrets
   - Add environment variables

4. **Logs**: View logs in Space → Logs tab

5. **Custom Domain**: Hugging Face Spaces come with HTTPS automatically

## Troubleshooting

**Build fails:**
- Check `requirements.txt` versions
- Ensure all dependencies are listed
- Check Dockerfile syntax

**Model not loading:**
- Verify model files are in `models/` directory
- Check file paths in code
- Ensure model files are committed to repo

**API not responding:**
- Check logs in Space → Logs
- Verify port is 7860 (Hugging Face default)
- Ensure app is binding to `0.0.0.0`

## Alternative: Using Gradio (Simpler)

If you want a simpler UI, you can use Gradio instead of Flask:

```python
import gradio as gr
import joblib

model = joblib.load('models/random_forest.joblib')

def predict(X, Y, Z, EDA, HR, TEMP):
    # Your prediction logic
    pred = model.predict([[X, Y, Z, EDA, HR, TEMP]])[0]
    return f"Predicted Stress Level: {pred}"

iface = gr.Interface(
    fn=predict,
    inputs=[
        gr.Number(label="X"),
        gr.Number(label="Y"),
        gr.Number(label="Z"),
        gr.Number(label="EDA"),
        gr.Number(label="HR"),
        gr.Number(label="TEMP")
    ],
    outputs="text",
    title="Stress Prediction"
)

iface.launch()
```

## Resources

- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Docker Spaces Guide](https://huggingface.co/docs/hub/spaces-sdks-docker)
- [Gradio Documentation](https://gradio.app/docs/)

