# Dashboard Hosting Guide

## Firebase Hosting Limitation

Firebase Hosting is for **static websites only** (HTML/CSS/JS). Since Dash apps are Python-based and require a server, they cannot be directly hosted on Firebase Hosting.

## Recommended Hosting Solutions

### 1. Heroku (Easiest) ⭐ Recommended

**Pros**: Easy setup, free tier available, great for Dash apps

**Steps**:
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Set environment variables:
   ```bash
   heroku config:set FIREBASE_ENABLED=true
   heroku config:set FIREBASE_CREDENTIAL=firebase_credentials.json
   ```
5. Deploy: `git push heroku main`

**Files needed**:
- `Procfile`: `web: gunicorn app:app` (already created)
- `requirements.txt` (already created)
- `runtime.txt` (already created)

### 2. Google Cloud Run

**Pros**: Pay per use, scales automatically

**Steps**:
1. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD gunicorn --bind 0.0.0.0:$PORT dashboard:app
   ```
2. Deploy: `gcloud run deploy`

### 3. Railway

**Pros**: Simple, modern interface

**Steps**:
1. Connect GitHub repo
2. Railway auto-detects Python
3. Set environment variables in dashboard
4. Deploy!

### 4. Render

**Pros**: Free tier, easy setup

**Steps**:
1. Connect GitHub repo
2. Select "Web Service"
3. Build command: `pip install -r requirements_dashboard.txt`
4. Start command: `python dashboard.py`
5. Set environment variables

## Using Firebase for Data Storage

Even though you can't host the dashboard on Firebase Hosting, you **can** use Firebase for data storage:

✅ **Firebase Firestore** - Store stress events
✅ **Firebase Realtime Database** - Real-time data sync
✅ **Firebase Authentication** - User management (optional)

The dashboard is already configured to save stress events to Firebase!

## Quick Start with Heroku

```bash
# 1. Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# 2. Login
heroku login

# 3. Initialize git (if not already)
git init
git add .
git commit -m "Initial commit"

# 4. Create Heroku app
heroku create your-stress-dashboard

# 5. Set environment variables
heroku config:set FIREBASE_ENABLED=true

# 6. Upload Firebase credentials (if using)
# You'll need to add firebase_credentials.json to Heroku config vars
# Or use environment variables for sensitive data

# 7. Deploy
git push heroku main

# 8. Open your app
heroku open
```

## Environment Variables for Production

Set these in your hosting platform:

- `FIREBASE_ENABLED`: `true` or `false`
- `FIREBASE_CREDENTIAL`: Path to credentials file (or use environment variables)
- `PORT`: Usually auto-set by hosting platform
- `MODEL_NAME`: Optional, defaults to `random_forest.joblib`

## Firebase Data Access

After deployment, stress events will be stored in Firebase and can be accessed:
- From Firebase Console
- Via Firebase Admin SDK
- Through Firebase REST API
- Using the `view_stress_events.py` script

