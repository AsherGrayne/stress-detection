# Render Deployment - Step by Step Guide

Complete guide to deploy your ML model API to Render in 10 minutes.

---

## Prerequisites

Before starting, make sure you have:
- ✅ Your code in a GitHub repository
- ✅ `models/` folder with `.joblib` files
- ✅ Python 3.10+ installed locally (for testing)

---

## Step 1: Prepare Your Files

### 1.1 Check Your Repository Structure

Your repository should have:
```
your-repo/
├── app.py (or huggingface_deploy.py)
├── requirements.txt
├── Procfile
├── models/
│   ├── random_forest.joblib
│   ├── gradient_boosting.joblib
│   ├── logistic_regression.joblib
│   └── mlp_classifier.joblib
└── README.md (optional)
```

### 1.2 Create/Update `app.py`

**Option A: Use existing `huggingface_deploy.py`**
- Rename `huggingface_deploy.py` to `app.py` OR
- Copy it as `app.py` in your repository

**Option B: Use existing `app.py`**
- Make sure it uses `os.environ.get('PORT', 7860)` for the port
- Ensure it loads models from the `models/` directory

### 1.3 Create/Update `requirements.txt`

Create or update `requirements.txt` with:
```
flask==2.3.0
flask-cors==4.0.0
scikit-learn==1.6.1
joblib==1.3.2
pandas==2.0.3
numpy==1.26.4
gunicorn==21.2.0
```

**Important**: Make sure `scikit-learn==1.6.1` matches your model version!

### 1.4 Create `Procfile`

Create a file named `Procfile` (no extension) in your root directory:

```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

**Note**: 
- `app:app` means: use `app.py` file, `app` variable (Flask instance)
- `$PORT` is automatically set by Render

### 1.5 Verify Your `app.py` Uses PORT

Make sure your `app.py` has:
```python
port = int(os.environ.get("PORT", 7860))
app.run(host='0.0.0.0', port=port, debug=False)
```

### 1.6 Commit Everything to GitHub

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

---

## Step 2: Create Render Account

### 2.1 Go to Render

1. Open your browser
2. Go to: **https://render.com**
3. Click **"Get Started for Free"** or **"Sign Up"**

### 2.2 Sign Up

**Option A: Sign up with GitHub (Recommended)**
1. Click **"Sign up with GitHub"**
2. Authorize Render to access your GitHub account
3. This automatically connects your repositories

**Option B: Sign up with Email**
1. Enter your email
2. Create a password
3. Verify your email
4. You'll need to connect GitHub later

---

## Step 3: Create New Web Service

### 3.1 Navigate to Dashboard

1. After signing in, you'll see the Render dashboard
2. Click the **"New +"** button (top right)
3. Select **"Web Service"**

### 3.2 Connect Repository

1. **If you signed up with GitHub:**
   - You'll see a list of your repositories
   - Find and click on your repository

2. **If you signed up with email:**
   - Click **"Connect GitHub"**
   - Authorize Render
   - Select your repository

### 3.3 Configure Service

Fill in the following:

**Basic Settings:**
- **Name**: `stress-prediction-api` (or your choice)`
- **Region**: Choose closest to you (e.g., `Oregon (US West)`)
- **Branch**: `main` (or `master` if that's your branch)
- **Root Directory**: Leave empty (unless your files are in a subfolder)

**Build & Deploy:**
- **Environment**: Select **`Python 3`**
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  gunicorn app:app --bind 0.0.0.0:$PORT
  ```

**Instance Type:**
- **Free**: 512 MB RAM, 0.1 CPU (good for testing)
- **Starter ($7/month)**: 512 MB RAM, 0.5 CPU (no cold starts)

**Advanced Settings (Optional):**
- Click **"Advanced"** to add environment variables:
  - `MODEL_NAME`: `random_forest.joblib`
  - `MODEL_DIR`: `models`
  - `PORT`: (auto-set, don't change)

### 3.4 Create Service

1. Review all settings
2. Click **"Create Web Service"**
3. Render will start building your service

---

## Step 4: Wait for Deployment

### 4.1 Build Process

You'll see the build logs:
1. **Cloning repository** - Downloads your code
2. **Installing dependencies** - Runs `pip install -r requirements.txt`
3. **Starting service** - Launches your app

**This takes 2-5 minutes**

### 4.2 Monitor Build

Watch the logs for:
- ✅ **"Build successful"**
- ✅ **"Starting service"**
- ✅ **"Your service is live"**

### 4.3 Check for Errors

If you see errors:
- **"Module not found"**: Check `requirements.txt`
- **"Port already in use"**: Check `Procfile` uses `$PORT`
- **"Model not found"**: Check `models/` folder is in repository

---

## Step 5: Get Your API URL

### 5.1 Find Your URL

Once deployed, you'll see:
- **Service URL**: `https://stress-prediction-api.onrender.com`

This is your API endpoint!

### 5.2 Test Your API

**Option A: Test in Browser**
1. Go to: `https://your-app-name.onrender.com`
2. You should see the API home page with endpoints

**Option B: Test with Python**

Update `test_hf_api.py`:
```python
import requests

url = "https://your-app-name.onrender.com/predict"

response = requests.post(url, json={
    "X": -21.0,
    "Y": -53.0,
    "Z": 27.0,
    "EDA": 0.213944,
    "HR": 75.07,
    "TEMP": 30.37
})

print(response.json())
```

Run:
```bash
python test_hf_api.py
```

---

## Step 6: Handle Cold Starts (Free Tier)

### 6.1 What is Cold Start?

On the **free tier**, your service:
- Spins down after **15 minutes** of inactivity
- First request after spin-down takes **30-60 seconds**
- Subsequent requests are fast

### 6.2 Solutions

**Option A: Upgrade to Starter Plan ($7/month)**
- No cold starts
- Always running
- Better performance

**Option B: Use a Keep-Alive Service**
- Use services like `uptimerobot.com` to ping your API every 10 minutes
- Keeps your service awake (free)

**Option C: Accept Cold Starts**
- Fine for testing/demos
- Users wait 30 seconds on first request

---

## Step 7: Update Your Code (If Needed)

### 7.1 Update Test Script

Update `test_hf_api.py`:
```python
import requests

# Update this URL to your Render URL
url = "https://your-app-name.onrender.com/predict"

response = requests.post(url, json={
    "X": -21.0,
    "Y": -53.0,
    "Z": 27.0,
    "EDA": 0.213944,
    "HR": 75.07,
    "TEMP": 30.37
})

print(response.json())
```

### 7.2 Update Dashboard (If Using)

If your dashboard calls the API, update the URL:
```python
API_URL = "https://your-app-name.onrender.com/predict"
```

---

## Troubleshooting

### Problem: Build Fails

**Solution:**
1. Check build logs in Render dashboard
2. Verify `requirements.txt` has all dependencies
3. Make sure Python version is compatible (3.10+)

### Problem: Service Crashes

**Solution:**
1. Check logs in Render dashboard
2. Verify `Procfile` is correct
3. Make sure `app.py` exists and has correct Flask app name

### Problem: Model Not Found

**Solution:**
1. Verify `models/` folder is in your repository
2. Check `.gitignore` doesn't exclude `.joblib` files
3. Verify model files are committed to git

### Problem: Port Error

**Solution:**
1. Make sure `Procfile` uses `$PORT`
2. Verify `app.py` uses `os.environ.get('PORT', 7860)`
3. Don't hardcode port numbers

### Problem: Slow First Request

**Solution:**
- This is normal on free tier (cold start)
- Upgrade to paid plan to avoid this
- Or use keep-alive service

---

## Quick Reference

### Your API Endpoints

- **Home**: `https://your-app-name.onrender.com/`
- **Health**: `https://your-app-name.onrender.com/health`
- **Predict**: `https://your-app-name.onrender.com/predict` (POST)

### Important Files

- `app.py` - Your Flask application
- `requirements.txt` - Python dependencies
- `Procfile` - Tells Render how to run your app
- `models/` - Your ML model files

### Environment Variables (Optional)

Set in Render dashboard → Environment:
- `MODEL_NAME`: `random_forest.joblib`
- `MODEL_DIR`: `models`

---

## Next Steps

1. ✅ **Test your API** with `test_hf_api.py`
2. ✅ **Update your dashboard** to use the new URL
3. ✅ **Set up monitoring** (optional)
4. ✅ **Consider upgrading** if you need no cold starts

---

## Summary

**What you did:**
1. Prepared files (`app.py`, `requirements.txt`, `Procfile`)
2. Created Render account
3. Connected GitHub repository
4. Configured and deployed web service
5. Got your API URL

**Your API is now live at:**
`https://your-app-name.onrender.com`

**Time taken:** ~10 minutes

**Cost:** Free (with cold starts) or $7/month (no cold starts)

---

## Need Help?

- **Render Docs**: https://render.com/docs
- **Render Support**: support@render.com
- **Check Logs**: Render dashboard → Your service → Logs

---

**Congratulations! Your ML API is now deployed on Render! 🎉**

