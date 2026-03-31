# 🔐 DVC + GitHub Secrets - Quick Reference Card

## 🚨 TODAY - 4 Steps to Secure Your Repository

### Step 1: Revoke Old Credentials (AWS Console)
```
Console → IAM → Users → Security credentials
├─ Find: AKIASAM27Y62G2GVBME4
├─ Action: DELETE
├─ Create: NEW Access Key
└─ Save: AKIA_NEW_... and SECRET_NEW_...
```

### Step 2: Local Setup (Your Machine)

**Windows Command Prompt:**
```batch
set AWS_ACCESS_KEY_ID=AKIA_NEW_...
set AWS_SECRET_ACCESS_KEY=SECRET_NEW_...
setup-dvc-local.bat
dvc pull
```

**Linux/Mac Terminal:**
```bash
export AWS_ACCESS_KEY_ID=AKIA_NEW_...
export AWS_SECRET_ACCESS_KEY=SECRET_NEW_...
bash setup-dvc-local.sh
dvc pull
```

### Step 3: Add GitHub Secrets

```
GitHub.com → Your Repo → Settings → Secrets and variables → Actions
├─ New Secret → AWS_ACCESS_KEY_ID = AKIA_NEW_...
└─ New Secret → AWS_SECRET_ACCESS_KEY = SECRET_NEW_...
```

### Step 4: Commit & Push

```bash
git add .dvc/config.template setup-dvc-local.* .gitignore
git add .github/workflows/cicd.yaml
git add *.md

git commit -m "chore: secure DVC with GitHub Secrets"
git push origin main
```

---

## ✅ Verification Checklist

```
Immediate (Do Today):
☐ AWS key AKIASAM27Y62G2GVBME4 DELETED
☐ NEW AWS credentials created
☐ Local: dvc pull works
☐ GitHub: AWS_ACCESS_KEY_ID secret added
☐ GitHub: AWS_SECRET_ACCESS_KEY secret added
☐ Pushed to main branch

Wait (5 minutes):
☐ GitHub Actions pipeline runs
☐ DVC Pull step shows ✅ PASSED
☐ No credentials in logs

Final Check (Tomorrow):
☐ .dvc/config.local created locally
☐ No .dvc/config with secrets in repo
☐ Can still run dvc pull successfully
```

---

## 🔧 Troubleshooting (Quick Fixes)

### Local dvc pull doesn't work
```bash
# Check if env vars are set
echo $AWS_ACCESS_KEY_ID

# If empty, set them again
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...

# Or run setup script
bash setup-dvc-local.sh
```

### GitHub Actions fails at DVC step
```
✓ Check GitHub Secrets exist (Settings → Secrets)
✓ Check secret names: AWS_ACCESS_KEY_ID (exact case)
✓ Check credentials are NEW (not the old AKIASAM27Y62G2GVBME4)
✓ Check AWS credentials have S3 permissions
```

### Still see AKIASAM27Y62G2GVBME4 in repo
```bash
# Search in history
git log --all -- .dvc/config | head -20

# This key MUST be revoked in AWS regardless
```

---

## 📁 File Reference

| File | Purpose | Commit? |
|------|---------|---------|
| `.dvc/config` | Template config | ✅ YES |
| `.dvc/config.local` | Credentials | ❌ NO (.gitignore) |
| `.dvc/config.template` | Dev reference | ✅ YES |
| `setup-dvc-local.sh` | Unix setup | ✅ YES |
| `setup-dvc-local.bat` | Windows setup | ✅ YES |
| `.github/workflows/cicd.yaml` | CI/CD pipeline | ✅ YES |
| `DVC_SECURITY.md` | Full guide | ✅ YES |

---

## 🔐 How It Works (Simplified)

```
LOCAL DEV              GitHub Actions           AWS S3
┌─────────────┐        ┌──────────────┐      ┌────────┐
│ .dvc/       │   or   │ GitHub       │  →   │ Bucket │
│ config.local│        │ Secrets      │      │        │
│ (env vars)  │        │ (env vars)   │      │ Data   │
└─────────────┘        └──────────────┘      └────────┘
   dvc pull              dvc pull              pulled
```

---

## 🚀 Environment Variables Quick Ref

```bash
# List set variables
echo $AWS_ACCESS_KEY_ID

# Set new variables (Session only - doesn't persist)
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...

# Check if set
[ -z "$AWS_ACCESS_KEY_ID" ] && echo "NOT SET" || echo "SET"

# Use in script
echo "Key: $AWS_ACCESS_KEY_ID"
```

---

## 📞 Common Commands

```bash
# Test credentials
dvc pull --verbose

# Check config
cat .dvc/config.local

# See environment
env | grep AWS

# Cleanup old setup
rm .dvc/config  # If it has credentials (recreate from template)

# Check gitignore
cat .gitignore | grep dvc
```

---

## ⏱️ Time Required

| Step | Time | Status |
|------|------|--------|
| Revoke AWS key | 5 min | DO NOW |
| Local setup | 10 min | DO NOW |
| GitHub Secrets | 5 min | DO NOW |
| Push changes | 5 min | DO NOW |
| Wait & verify | 5 min | DO NOW |
| **TOTAL** | **30 min** | **~1 hour to full security** |

---

## ❌ DON'Ts (To Avoid Disaster)

```
❌ DON'T commit .dvc/config with secrets
❌ DON'T push credentials to any branch
❌ DON'T hardcode credentials in code
❌ DON'T share credentials in chat/email
❌ DON'T use old AKIASAM27Y62G2GVBME4 key
❌ DON'T forget to delete AWS old key
❌ DON'T skip GitHub Secrets step
❌ DON'T push before you can dvc pull locally
```

---

## ✅ DOs (Best Practices)

```
✅ DO use environment variables locally
✅ DO use GitHub Secrets for CI/CD
✅ DO rotate credentials every 6 months
✅ DO check .gitignore has .dvc/config
✅ DO test locally before pushing
✅ DO monitor AWS for unauthorized access
✅ DO document where credentials are stored
✅ DO revoke old keys immediately
```

---

## 📊 Status Checklist

### Before (Current - INSECURE) 🚨
```
❌ Credentials in .dvc/config
❌ Credentials visible in Git history
❌ Anyone can access your S3 bucket
❌ No CI/CD pipeline protection
❌ Manual credential rotation
```

### After (Your Goal - SECURE) ✅
```
✅ Credentials in .gitignore
✅ No credentials in Git
✅ S3 bucket protected
✅ CI/CD uses GitHub Secrets
✅ Easy credential rotation
```

---

## 🎯 Today's Goal

```
9 AM:  Read this file + DVC_SECURITY_VISUAL_GUIDE.md
10 AM: Complete 4 steps above
11 AM: Verify everything works
12 PM: SECURE! 🎉
```

---

## 📖 Read Next

Complete guides:
1. `DVC_SECURITY_VISUAL_GUIDE.md` ← Visual explanations
2. `GITHUB_SECRETS_SETUP.md` ← Step-by-step checklist
3. `DVC_SECURITY.md` ← Complete reference
4. `DVC_SECURITY_IMPLEMENTATION.md` ← Full summary

---

## 🆘 Emergency

Credentials compromised?

```
1. DELETE old AWS key immediately
   AWS Console → IAM → Delete access key

2. CREATE new AWS credentials

3. Update GitHub Secrets with NEW credentials

4. Run: dvc pull (verify it works)

5. Monitor AWS for unauthorized access
   CloudTrail → Look for unknown activity
```

---

## Quick Decision Tree

```
"dvc pull fails locally"
  ├─ Are AWS_ACCESS_KEY_ID env vars set?
  │  ├─ No → Run setup script
  │  └─ Yes → Credentials might be wrong
  │
  └─ Environment variables correct?
     ├─ No → Check AWS console for new credentials
     └─ Yes → Your S3 bucket might be wrong

"GitHub Actions dvc pull fails"
  ├─ GitHub Secrets added?
  │  ├─ No → Add them now
  │  └─ Yes → Continue
  │
  └─ Secret names correct?
     ├─ No → Names must be AWS_ACCESS_KEY_ID (exact)
     └─ Yes → Credentials might be wrong
```

---

**Status**: Ready to implement    
**Difficulty**: Easy (5/5 files already created)    
**Time**: 30 minutes total    
**Result**: Your credentials are now secure! 🔒
