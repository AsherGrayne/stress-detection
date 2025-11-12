# Quick Deploy to Render (5 Minutes)

## Step 1: Prepare Your Files

Make sure you have these files in your repository:
- ✅ `app.py` (or copy `huggingface_deploy.py` as `app.py`)
- ✅ `requirements.txt`
- ✅ `models/` folder with `.joblib` files
- ✅ `Procfile` (optional, but recommended)

## Step 2: Create Procfile (if not exists)

Create `Procfile` in your root directory:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

## Step 3: Update requirements.txt

Make sure `requirements.txt` includes:
```
flask==2.3.0
flask-cors==4.0.0
scikit-learn==1.6.1
joblib==1.3.2
pandas==2.0.3
numpy==1.26.4
gunicorn==21.2.0
```

## Step 4: Deploy to Render

1. **Go to**: https://render.com
2. **Sign up** with GitHub
3. **Click**: "New +" → "Web Service"
4. **Connect** your GitHub repository
5. **Configure**:
   - **Name**: `stress-prediction-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Instance Type**: Free
6. **Click**: "Create Web Service"

## Step 5: Wait for Deployment

- Build takes ~2-3 minutes
- Your API will be at: `https://stress-prediction-api.onrender.com`

## Step 6: Test

Update `test_hf_api.py`:
```python
url = "https://stress-prediction-api.onrender.com/predict"
```

Then test:
```bash
python test_hf_api.py
```

## Troubleshooting

### Cold Start Issue
- Free tier spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- Consider upgrading to paid plan ($7/month) to avoid cold starts

### Model Loading Error
- Make sure `models/` folder is in your repository
- Check that model files are committed to git
- Verify `MODEL_DIR` environment variable if needed

### Port Error
- Render sets `PORT` environment variable automatically
- Make sure your app uses `os.environ.get('PORT', 5000)`

## That's It!

Your API is now live on Render! 🎉

