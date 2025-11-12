# Fix Hugging Face Authentication

## Problem
Git push fails with: "Password authentication in git is no longer supported"

## Solution: Use Access Token

### Step 1: Create Access Token

1. Go to: https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Fill in:
   - **Name**: `git-push-token` (or any name)
   - **Type**: Select **"Write"** (needed to push)
4. Click **"Generate token"**
5. **IMPORTANT**: Copy the token immediately (you won't see it again!)
   - It looks like: `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 2: Use Token for Git Push

**Option A: Use token in URL (One-time)**

When Git asks for password, use your token:

```powershell
# When prompted:
# Username: YOUR_HF_USERNAME
# Password: PASTE_YOUR_TOKEN_HERE (the hf_xxxxx token)
```

**Option B: Update Git Remote URL (Recommended)**

Update your Git remote to include the token:

```powershell
# Replace YOUR_USERNAME and YOUR_TOKEN
git remote set-url origin https://YOUR_USERNAME:YOUR_TOKEN@huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

# Then push
git push
```

**Option C: Use Git Credential Manager (Best for Windows)**

```powershell
# Configure Git to use credential manager
git config --global credential.helper manager-core

# Then try push again - it will prompt and save credentials
git push
```

### Step 3: Push Again

After setting up the token, try pushing:

```powershell
git push
```

## Quick Fix (Copy-Paste Ready)

1. Get your token from: https://huggingface.co/settings/tokens
2. Run this (replace YOUR_USERNAME and YOUR_TOKEN):

```powershell
git remote set-url origin https://YOUR_USERNAME:YOUR_TOKEN@huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
git push
```

## Security Note

- Never commit your token to Git
- If you accidentally share it, revoke it and create a new one
- Tokens with "Write" access can push to your repos

