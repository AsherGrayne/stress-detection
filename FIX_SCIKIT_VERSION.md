# Fix Scikit-Learn Version Mismatch

## Problem
Model was saved with scikit-learn 1.6.1, but Hugging Face is using 1.7.2, causing loading to fail.

## Solution: Pin scikit-learn Version

Update `requirements.txt` in your Space to use the same version that was used to train the model.

### Step 1: Update requirements.txt

In your Space folder, edit `requirements.txt` and change:

```
scikit-learn>=1.2.0
```

To:

```
scikit-learn==1.6.1
```

Or if you want to be more flexible but still compatible:

```
scikit-learn>=1.6.1,<1.7.0
```

### Step 2: Commit and Push

```powershell
# In your Space folder
cd stress-prediction-api

# Edit requirements.txt (use the version below)
# Then:
git add requirements.txt
git commit -m "Fix scikit-learn version compatibility"
git push
```

### Step 3: Wait for Rebuild

The Space will rebuild with the correct scikit-learn version.

## Complete requirements.txt

Here's what your `requirements.txt` should look like:

```
flask==2.3.0
flask-cors==4.0.0
scikit-learn==1.6.1
joblib==1.3.2
pandas==2.0.3
numpy==1.24.3
```

Or with compatible ranges:

```
flask>=2.3.0
flask-cors>=4.0.0
scikit-learn>=1.6.1,<1.7.0
joblib>=1.3.2
pandas>=2.0.3
numpy>=1.24.3,<2.0.0
```

## Alternative: Retrain with Current Version

If you can't use the old version, you would need to retrain your models with scikit-learn 1.7.2, but that's more work.

## Quick Fix (Copy-Paste)

```powershell
cd stress-prediction-api

# Create/update requirements.txt with:
@"
flask==2.3.0
flask-cors==4.0.0
scikit-learn==1.6.1
joblib==1.3.2
pandas==2.0.3
numpy==1.24.3
"@ | Out-File -FilePath requirements.txt -Encoding utf8

git add requirements.txt
git commit -m "Fix scikit-learn version to 1.6.1"
git push
```

