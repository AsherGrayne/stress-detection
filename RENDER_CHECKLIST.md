# Render Deployment Checklist

Quick checklist to deploy to Render in 10 minutes.

## ✅ Pre-Deployment Checklist

### Files Required
- [ ] `app.py` exists (or `huggingface_deploy.py` renamed to `app.py`)
- [ ] `requirements.txt` exists with all dependencies
- [ ] `Procfile` exists with: `web: gunicorn app:app --bind 0.0.0.0:$PORT`
- [ ] `models/` folder exists with `.joblib` files
- [ ] All files committed to GitHub

### Code Checks
- [ ] `app.py` uses `os.environ.get('PORT', 7860)` for port
- [ ] `app.py` runs with `app.run(host='0.0.0.0', port=port)`
- [ ] Model loading path is correct (`models/` directory)
- [ ] All imports are in `requirements.txt`

---

## 🚀 Deployment Steps

### Step 1: Prepare Files (2 minutes)
- [ ] Verify `requirements.txt` has:
  ```
  flask==2.3.0
  flask-cors==4.0.0
  scikit-learn==1.6.1
  joblib==1.3.2
  pandas==2.0.3
  numpy==1.26.4
  gunicorn==21.2.0
  ```

- [ ] Verify `Procfile` has:
  ```
  web: gunicorn app:app --bind 0.0.0.0:$PORT
  ```

- [ ] Make sure `app.py` exists (or copy `huggingface_deploy.py` as `app.py`)

- [ ] Commit to GitHub:
  ```bash
  git add .
  git commit -m "Prepare for Render"
  git push
  ```

### Step 2: Create Render Account (1 minute)
- [ ] Go to https://render.com
- [ ] Sign up with GitHub (recommended)
- [ ] Verify email if needed

### Step 3: Create Web Service (3 minutes)
- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub repository
- [ ] Select your repository
- [ ] Configure:
  - Name: `stress-prediction-api`
  - Environment: `Python 3`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
  - Instance: Free
- [ ] Click "Create Web Service"

### Step 4: Wait for Build (2-5 minutes)
- [ ] Watch build logs
- [ ] Wait for "Build successful"
- [ ] Wait for "Service is live"
- [ ] Note your service URL

### Step 5: Test (1 minute)
- [ ] Open service URL in browser
- [ ] Test with `test_render_api.py`
- [ ] Verify predictions work

---

## 📝 Quick Commands

### Update Procfile
```bash
echo "web: gunicorn app:app --bind 0.0.0.0:\$PORT" > Procfile
```

### Test Locally First
```bash
pip install -r requirements.txt
gunicorn app:app --bind 0.0.0.0:5000
```

### Update Test Script
Edit `test_render_api.py`:
```python
RENDER_URL = "https://your-app-name.onrender.com"
```

---

## 🐛 Common Issues

### Build Fails
- [ ] Check `requirements.txt` has all dependencies
- [ ] Verify Python version compatibility
- [ ] Check build logs for errors

### Service Crashes
- [ ] Verify `Procfile` is correct
- [ ] Check `app.py` exists
- [ ] Verify Flask app variable is named `app`

### Model Not Found
- [ ] Check `models/` folder is in repository
- [ ] Verify `.gitignore` doesn't exclude `.joblib`
- [ ] Check model files are committed

### Port Error
- [ ] Verify `Procfile` uses `$PORT`
- [ ] Check `app.py` uses `os.environ.get('PORT')`

---

## ✅ Post-Deployment

- [ ] Save your service URL
- [ ] Update `test_render_api.py` with your URL
- [ ] Test all endpoints
- [ ] Update dashboard/client code with new URL
- [ ] Set up monitoring (optional)

---

## 📞 Need Help?

- Render Docs: https://render.com/docs
- Check Logs: Dashboard → Your Service → Logs
- Support: support@render.com

---

**Time to Deploy: ~10 minutes** ⏱️

**Cost: Free (with cold starts) or $7/month (no cold starts)** 💰

