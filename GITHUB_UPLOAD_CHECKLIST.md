# GitHub Upload Checklist for Render Deployment

## ✅ Files You MUST Include

### Core Application Files
- ✅ `app.py` (or `huggingface_deploy.py` renamed as `app.py`)
- ✅ `requirements.txt`
- ✅ `Procfile`
- ✅ `models/` folder with all `.joblib` files:
  - `random_forest.joblib`
  - `gradient_boosting.joblib`
  - `logistic_regression.joblib`
  - `mlp_classifier.joblib`

### Optional but Recommended
- ✅ `README.md` (documentation)
- ✅ `test_render_api.py` (for testing)

## ❌ Files You Should EXCLUDE

### Large Data Files (GitHub has 100MB file limit)
- ❌ `balanced_data.csv` (if large)
- ❌ `Stress-Lysis.csv` (if large)
- ❌ `merged_data.csv` (if large)
- ❌ Any other large CSV files

### Sensitive/Personal Files
- ❌ `firebase_credentials.json` (if exists)
- ❌ `.env` files with secrets
- ❌ Any API keys or tokens

### Temporary/Test Files
- ❌ `sensor_data.json` (generated file)
- ❌ `__pycache__/` folders
- ❌ `*.pyc` files
- ❌ `.pytest_cache/`
- ❌ Test scripts (optional, but not needed for deployment)

### Already Deployed Files
- ❌ `stress-prediction-api/` folder (if you're deploying the root)

## 📝 Quick Steps

### 1. Create `.gitignore` File

Create a `.gitignore` file in your root directory:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Data files (large)
*.csv
*.json
!requirements*.txt

# Sensitive files
firebase_credentials.json
.env
*.key
*.pem

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Test files (optional)
test_*.py
*_test.py
```

### 2. Prepare Your Repository

**Option A: Upload Everything (Recommended for First Time)**
- Upload all files
- GitHub will warn about large files
- You can remove them later if needed

**Option B: Upload Only What's Needed**
- Only upload files listed in "MUST Include" section
- Cleaner repository
- Faster upload

### 3. Minimum Files for Render

At minimum, you need:
```
your-repo/
├── app.py                    # Your Flask app
├── requirements.txt          # Dependencies
├── Procfile                  # Render config
└── models/
    ├── random_forest.joblib
    ├── gradient_boosting.joblib
    ├── logistic_regression.joblib
    └── mlp_classifier.joblib
```

## 🚀 After Uploading to GitHub

1. **Verify Files Are There**
   - Check that `app.py` exists
   - Check that `models/` folder is uploaded
   - Check that `requirements.txt` is there
   - Check that `Procfile` is there

2. **Test Repository**
   - Clone it to a new folder
   - Verify all files are present

3. **Then Deploy to Render**
   - Go to render.com
   - Connect your GitHub repository
   - Deploy!

## ⚠️ Important Notes

### Large Files Warning
- If your CSV files are large (>100MB), GitHub will reject them
- You can use Git LFS (Large File Storage) if needed
- Or simply exclude them (not needed for API deployment)

### Model Files
- `.joblib` files are usually fine (even if 10-50MB)
- GitHub allows files up to 100MB
- If models are larger, consider Git LFS

### Private vs Public
- **Private repository**: Only you can see it
- **Public repository**: Anyone can see it
- Render works with both

## ✅ Final Checklist Before Uploading

- [ ] `app.py` exists (or `huggingface_deploy.py` renamed)
- [ ] `requirements.txt` has all dependencies
- [ ] `Procfile` has: `web: gunicorn app:app --bind 0.0.0.0:$PORT`
- [ ] `models/` folder with `.joblib` files
- [ ] `.gitignore` created (to exclude large/sensitive files)
- [ ] No sensitive credentials in files
- [ ] README.md (optional but recommended)

## 🎯 Quick Command Reference

If you want to use Git commands:

```bash
# Initialize git (if not already)
git init

# Add files
git add app.py requirements.txt Procfile models/

# Commit
git commit -m "Initial commit for Render deployment"

# Add remote (after creating GitHub repo)
git remote add origin https://github.com/yourusername/your-repo.git

# Push
git push -u origin main
```

---

**Once uploaded to GitHub, you're ready to deploy to Render!** 🚀

