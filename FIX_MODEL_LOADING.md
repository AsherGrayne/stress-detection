# Fix Model Not Loading Issue

## Problem
API shows `"model": "not loaded"` - the model failed to load during startup.

## Common Causes & Solutions

### 1. Check if Models Folder Exists

In your Space repository, verify you have:
```
models/
  ├── random_forest.joblib
  ├── logistic_regression.joblib
  └── ... (other .joblib files)
```

### 2. Check Model Loading Code

The code tries to load: `models/random_forest.joblib`

Make sure:
- The `models/` folder is in your Space
- The `.joblib` files are inside `models/` folder
- File names match exactly (case-sensitive)

### 3. Check Logs for Error Messages

1. Go to your Space page
2. Click **"Logs"** tab
3. Look for error messages like:
   - `FileNotFoundError`
   - `No such file or directory`
   - `Error loading model: ...`

### 4. Quick Fix: Update app.py to Show More Info

Add better error handling to see what's wrong:

```python
# In app.py, update the model loading section:
print(f"Loading model: {MODEL_NAME}")
print(f"Model directory: {MODEL_DIR}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in current dir: {os.listdir('.')}")

if os.path.exists(MODEL_DIR):
    print(f"Models directory exists!")
    print(f"Files in models/: {os.listdir(MODEL_DIR)}")
else:
    print(f"ERROR: Models directory '{MODEL_DIR}' does not exist!")

try:
    model_path = os.path.join(MODEL_DIR, MODEL_NAME)
    print(f"Trying to load: {model_path}")
    if os.path.exists(model_path):
        print(f"File exists!")
        model = joblib.load(model_path)
        print("Model loaded successfully!")
    else:
        print(f"ERROR: Model file not found at {model_path}")
        model = None
except Exception as e:
    print(f"Error loading model: {e}")
    import traceback
    traceback.print_exc()
    model = None
```

### 5. Verify Files Are Committed

Make sure all files are pushed to Git:

```powershell
# In your Space folder
cd stress-prediction-api

# Check what files are there
git status

# If models/ is missing, add it
git add models/
git commit -m "Add models"
git push
```

### 6. Check Dockerfile

Make sure Dockerfile copies the models:

```dockerfile
COPY models/ ./models/
```

## Quick Diagnostic Steps

1. **Check Space Files:**
   - Go to Space → "Files and versions"
   - Verify `models/` folder exists
   - Verify `.joblib` files are inside

2. **Check Logs:**
   - Look for specific error messages
   - Check if model path is correct

3. **Test Locally First:**
   - Make sure models load on your computer
   - Verify file paths are correct

## Most Likely Issue

The `models/` folder or `.joblib` files weren't uploaded to the Space. 

**Fix:**
```powershell
# In your Space folder
cd stress-prediction-api

# Make sure models are there
ls models/

# If empty or missing, copy from parent
Copy-Item -Recurse ..\models .

# Commit and push
git add models/
git commit -m "Add model files"
git push
```

