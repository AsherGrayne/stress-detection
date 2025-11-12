# Quick Deploy to Hugging Face - Step by Step

## After Creating Your Space

### Step 1: Get Your Space Git URL

1. Go to your Space page on Hugging Face
2. Click the **"Files and versions"** tab
3. You'll see a section that says "Clone your repository"
4. Copy the Git URL (looks like: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`)

### Step 2: Clone Your Space Repository

Open terminal/PowerShell in your project folder and run:

```bash
# Replace with your actual Space URL
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME
```

### Step 3: Copy Required Files

From your project directory, copy these files into the cloned Space folder:

**Windows PowerShell:**
```powershell
# Make sure you're in the Space folder first
cd YOUR_SPACE_NAME

# Copy the Flask app (rename it to app.py)
Copy-Item ..\huggingface_deploy.py app.py

# Copy Dockerfile
Copy-Item ..\Dockerfile.hf Dockerfile

# Copy README
Copy-Item ..\README.hf.md README.md

# Copy requirements
Copy-Item ..\requirements.txt .

# Copy predict.py (needed for helper functions)
Copy-Item ..\predict.py .

# Copy models directory
Copy-Item -Recurse ..\models .
```

**Linux/Mac:**
```bash
# Make sure you're in the Space folder first
cd YOUR_SPACE_NAME

# Copy files
cp ../huggingface_deploy.py app.py
cp ../Dockerfile.hf Dockerfile
cp ../README.hf.md README.md
cp ../requirements.txt .
cp ../predict.py .
cp -r ../models .
```

### Step 4: Commit and Push

```bash
# Add all files
git add .

# Commit
git commit -m "Add ML model API"

# Push to Hugging Face
git push
```

### Step 5: Wait for Build

1. Go back to your Space page on Hugging Face
2. Click the **"Logs"** tab
3. Watch the build process (takes 2-5 minutes)
4. When you see "Running", your API is ready!

---

## Option 2: Using Web Interface (Alternative)

If you prefer not to use Git:

### Step 1: Prepare Files

Make sure you have these files ready:
- `huggingface_deploy.py` (will rename to `app.py`)
- `Dockerfile.hf` (will rename to `Dockerfile`)
- `README.hf.md` (will rename to `README.md`)
- `requirements.txt`
- `predict.py`
- All `.joblib` files from `models/` folder

### Step 2: Upload Files

1. Go to your Space page
2. Click **"Files and versions"** tab
3. Click **"Add file"** → **"Upload files"**
4. Upload files one by one:
   - Upload `huggingface_deploy.py` → Rename it to `app.py` in the interface
   - Upload `Dockerfile.hf` → Rename to `Dockerfile`
   - Upload `README.hf.md` → Rename to `README.md`
   - Upload `requirements.txt`
   - Upload `predict.py`
   - Upload all `.joblib` files from your `models/` folder

### Step 3: Create Models Directory Structure

In the web interface:
1. Click **"Add file"** → **"Create a new file"**
2. Create a file at path: `models/.gitkeep` (this creates the directory)
3. Then upload your `.joblib` files to the `models/` folder

### Step 4: Wait for Build

The Space will automatically rebuild when files are uploaded.

---

## Verify Your Files

Your Space should have these files:
```
YOUR_SPACE_NAME/
├── app.py                    (from huggingface_deploy.py)
├── Dockerfile                (from Dockerfile.hf)
├── README.md                 (from README.hf.md)
├── requirements.txt
├── predict.py
└── models/
    ├── random_forest.joblib
    ├── logistic_regression.joblib
    └── ... (other .joblib files)
```

## Test Your API

Once the build completes and shows "Running":

1. Your API URL will be: `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space`
2. Test it:
   ```python
   import requests
   
   url = "https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/predict"
   
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

## Troubleshooting

**Build fails?**
- Check the Logs tab for error messages
- Make sure all files are uploaded
- Verify `requirements.txt` has all dependencies

**Model not loading?**
- Ensure `.joblib` files are in `models/` folder
- Check file paths in `app.py`

**API not responding?**
- Wait for build to complete (status should be "Running")
- Check Logs tab for runtime errors

