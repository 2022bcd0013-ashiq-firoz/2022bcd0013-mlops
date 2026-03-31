# 🔐 GitHub Secrets Setup Checklist

## ⏱️ Takes 5 minutes

### Step 1: Generate New AWS Credentials
- [ ] Go to AWS Console: https://console.aws.amazon.com/
- [ ] Navigate to IAM → Users → Your User
- [ ] Go to "Security credentials" tab
- [ ] Create a new access key (delete the old one: `AKIASAM27Y62G2GVBME4`)
- [ ] Copy and save the new:
  - Access Key ID: `AKIA...`
  - Secret Access Key: `...`

### Step 2: Add Secrets to GitHub

#### Via GitHub Web UI (Easiest)
1. Go to your repo: https://github.com/YOUR_REPO
2. Click **Settings** (top right)
3. Left sidebar → **Secrets and variables** → **Actions**
4. Click **New repository secret**

**First Secret:**
- Name: `AWS_ACCESS_KEY_ID`
- Value: `AKIA...` (from Step 1)
- Click Add Secret

**Second Secret:**
- Name: `AWS_SECRET_ACCESS_KEY`
- Value: `...` (from Step 1)
- Click Add Secret

#### Via GitHub CLI (If you prefer terminal)
```bash
# Install GitHub CLI
# https://cli.github.com/

# Login to GitHub
gh auth login

# Add secrets to your repo
gh secret set AWS_ACCESS_KEY_ID --body "AKIA..."
gh secret set AWS_SECRET_ACCESS_KEY --body "..."

# Verify secrets are set
gh secret list
```

### Step 3: Verify Locally

```bash
# Set environment variables
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="..."

# Run setup script
bash setup-dvc-local.sh

# Test DVC pull
dvc pull -v
```

### Step 4: Commit and Push

```bash
# Stage changes (no .dvc/config - it's in .gitignore!)
git add .dvc/config.template setup-dvc-local.* .gitignore DVC_SECURITY.md

# Commit
git commit -m "chore: secure DVC configuration with GitHub Secrets"

# Push
git push origin main

# GitHub Actions should now pass the DVC step!
```

### Step 5: Monitor GitHub Actions

1. Go to your repo
2. Click **Actions** tab
3. Watch the pipeline run
4. ✅ DVC Pull step should succeed

---

## 🧪 Verify Secrets Are Working

After first successful run:

1. **Check workflow logs:**
   ```
   Repository → Actions → Latest run
   ```
   
2. **You should see:**
   ```
   ✅ Configure DVC with AWS credentials - PASSED
   ✅ Pull data from DVC remote - PASSED
   ```

3. **You should NOT see:**
   - Your actual access key
   - Your actual secret key
   - GitHub shows `***` for secrets in logs

---

## 📝 Completed Files

After following these steps, your setup includes:

```
✅ .gitignore              - Updated with .dvc/config
✅ .dvc/config.template    - Template without secrets
✅ .dvc/config.local       - Local config with YOUR credentials (not committed)
✅ setup-dvc-local.sh      - Bash script to setup local config
✅ setup-dvc-local.bat     - Batch script for Windows
✅ .github/workflows/cicd.yaml - Updated to use GitHub Secrets
✅ DVC_SECURITY.md         - Full security guide
✅ GitHub Repository Secrets - AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
```

---

## ❌ What NOT to Do

- ❌ Commit `.dvc/config` with credentials
- ❌ Hardcode credentials in Python code
- ❌ Push credentials to any branch
- ❌ Keep old compromised credentials
- ❌ Use personal AWS root account keys
- ❌ Share access keys between projects

---

## ✅ You're Done When

- [ ] Old AWS credentials revoked
- [ ] New credentials created
- [ ] Both secrets added to GitHub
- [ ] `.dvc/config` is in `.gitignore`
- [ ] Local `dvc pull` works
- [ ] GitHub Actions pipeline passes
- [ ] No credentials visible in logs

---

## 🆘 Help

**Still not working?**
1. Check GitHub Actions logs for error messages
2. Verify secret names: `AWS_ACCESS_KEY_ID` (exact case)
3. Verify new credentials have S3 permissions in AWS IAM
4. Re-read `DVC_SECURITY.md` for detailed troubleshooting
