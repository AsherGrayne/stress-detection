# Firebase Setup Guide

## Overview

This guide explains how to set up Firebase for storing stress events from your dashboard.

## Firebase Hosting Limitations

**Important**: Firebase Hosting is designed for static websites (HTML, CSS, JS). Dash apps are Python-based and require a server, so they cannot be directly hosted on Firebase Hosting.

### Alternatives for Hosting:
1. **Heroku** - Easy deployment for Dash apps
2. **Google Cloud Run** - Container-based hosting
3. **AWS Elastic Beanstalk** - Python app hosting
4. **Railway** - Simple deployment platform
5. **Render** - Free tier available

However, you can use **Firebase Realtime Database** or **Firestore** to store your stress events data, which works great with any hosting solution!

## Setup Steps

### 1. Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add Project"
3. Enter project name (e.g., "stress-monitor")
4. Follow the setup wizard

### 2. Enable Firestore Database

1. In Firebase Console, go to "Firestore Database"
2. Click "Create Database"
3. Choose "Start in test mode" (for development)
4. Select a location for your database

### 3. Get Service Account Credentials

1. Go to Project Settings (gear icon)
2. Click "Service Accounts" tab
3. Click "Generate New Private Key"
4. Save the JSON file as `firebase_credentials.json` in your project directory
5. **IMPORTANT**: Add `firebase_credentials.json` to `.gitignore` to keep it secure!

### 4. Install Firebase Admin SDK

```bash
pip install firebase-admin
```

### 5. Configure the Dashboard

Set environment variables:

**Windows (PowerShell):**
```powershell
$env:FIREBASE_ENABLED="true"
$env:FIREBASE_CREDENTIAL="firebase_credentials.json"
```

**Linux/Mac:**
```bash
export FIREBASE_ENABLED=true
export FIREBASE_CREDENTIAL=firebase_credentials.json
```

Or create a `.env` file:
```
FIREBASE_ENABLED=true
FIREBASE_CREDENTIAL=firebase_credentials.json
```

### 6. Run the Dashboard

```bash
python dashboard.py
```

The dashboard will now automatically save stress events (levels 1 and 2) to Firebase!

## Data Structure

Stress events are stored in Firestore with this structure:

```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "timestamp_readable": "2024-01-15T10:30:45.123456",
  "stress_level": 2.0,
  "confidence": 0.95,
  "model_name": "random_forest",
  "sensor_data": {
    "X": -21.0,
    "Y": -53.0,
    "Z": 27.0,
    "EDA": 0.213944,
    "HR": 75.07,
    "TEMP": 30.37
  }
}
```

## Viewing Stress Events

You can view stored events in:
1. Firebase Console → Firestore Database
2. Or use the `view_stress_events.py` script

## Security Rules (Production)

For production, update Firestore security rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /stress_events/{document=**} {
      // Allow read/write only for authenticated users
      allow read, write: if request.auth != null;
    }
  }
}
```

## Alternative: Firebase Realtime Database

If you prefer Realtime Database:

1. Go to "Realtime Database" in Firebase Console
2. Create database
3. Copy the database URL
4. Update `firebase_config.py` to use Realtime DB instead of Firestore

## Troubleshooting

- **"Firebase not initialized"**: Check that `firebase_credentials.json` exists and path is correct
- **Permission errors**: Make sure service account has proper permissions
- **Import errors**: Run `pip install firebase-admin`

