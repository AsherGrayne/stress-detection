# Git Commands to Upload Files to GitHub

Run these commands in PowerShell (one by one):

## Step 1: Navigate to Your Directory

```powershell
cd C:\Users\profe\Desktop\merged_data.csv
```

## Step 2: Check Current Status

```powershell
git status
```

## Step 3: Add Essential Files for Render

```powershell
# Add core application files
git add app.py
git add huggingface_deploy.py
git add requirements.txt
git add Procfile
git add runtime.txt

# Add model files
git add models/

# Add prediction scripts
git add predict.py
git add predict_single.py

# Add test files
git add test_render_api.py
git add test_api.py
git add test_hf_api.py

# Add documentation
git add *.md

# Add .gitignore
git add .gitignore
```

## Step 4: Add Other Python Files (Optional)

```powershell
# Add other Python scripts
git add *.py

# Add other config files
git add requirements_dashboard.txt
git add requirements_pico.txt
```

## Step 5: Check What Will Be Committed

```powershell
git status
```

This shows you what files are staged (will be uploaded).

## Step 6: Commit the Files

```powershell
git commit -m "Add files for Render deployment"
```

## Step 7: Push to GitHub

```powershell
git push origin main
```

---

## Alternative: Add Everything at Once

If you want to add all files (except those in .gitignore):

```powershell
# Add all files
git add .

# Check status
git status

# Commit
git commit -m "Upload all files for Render deployment"

# Push
git push origin main
```

---

## What Gets Excluded (via .gitignore)

These files will NOT be uploaded:
- ❌ `*.csv` (large data files)
- ❌ `*.json` (except requirements files)
- ❌ `__pycache__/` (Python cache)
- ❌ `firebase_credentials.json` (sensitive)
- ❌ `sensor_data.json` (generated file)

---

## Verify Upload

After pushing, check your GitHub repository to confirm:
- ✅ `app.py` is there
- ✅ `requirements.txt` is there
- ✅ `Procfile` is there
- ✅ `models/` folder with `.joblib` files is there

---

## Quick Copy-Paste (All at Once)

```powershell
cd C:\Users\profe\Desktop\merged_data.csv
git add .
git commit -m "Upload files for Render deployment"
git push origin main
```

This will add all files except those in `.gitignore`.

