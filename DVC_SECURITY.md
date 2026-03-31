# 🔐 DVC + AWS Credentials Security Guide

## ⚠️ Critical Security Issue

Your `.dvc/config` file currently contains **exposed AWS credentials**. This must be fixed immediately.

## 🚨 Immediate Actions Required

1. **Revoke AWS Credentials**
   - Go to AWS Console → IAM → Users → Select your user
   - Delete the old access key with ID `AKIASAM27Y62G2GVBME4`
   - Create a **new access key pair**

2. **Remove Credentials from Git History**
   ```bash
   # Remove from Git history
   git filter-branch --tree-filter 'rm -f .dvc/config' -- --all
   
   # Force push (carefully - coordinate with team)
   git push origin --force --all
   ```

3. **Add to .gitignore**
   Already done: `.dvc/config` is now in `.gitignore`

---

## ✅ Safe Implementation Steps

### For Local Development

#### Option A: Using Environment Variables (Recommended)

```bash
# Linux/macOS - Add to ~/.bashrc or ~/.zshrc
export AWS_ACCESS_KEY_ID="your_new_access_key"
export AWS_SECRET_ACCESS_KEY="your_new_secret_key"

# Windows - Set environment variables
set AWS_ACCESS_KEY_ID=your_new_access_key
set AWS_SECRET_ACCESS_KEY=your_new_secret_key
```

Then run setup script:
```bash
# Linux/macOS
bash setup-dvc-local.sh

# Windows
setup-dvc-local.bat
```

#### Option B: Using .dvc/config.local (Not committed to Git)

```bash
# Create .dvc/config.local with credentials
cat > .dvc/config.local << EOF
['remote "myremote"']
    url = s3://2022bcd0013-mlops/mlops-assignment
    access_key_id = YOUR_NEW_ACCESS_KEY
    secret_access_key = YOUR_NEW_SECRET_KEY
EOF

# Verify it's in .gitignore
dvc pull
```

---

### For GitHub Actions CI/CD

#### Step 1: Add Secrets to GitHub Repository

1. Go to your GitHub repository
2. Settings → Secrets and Variables → Actions → New repository secret
3. Add two secrets:
   - **Name**: `AWS_ACCESS_KEY_ID` | **Value**: Your new access key
   - **Name**: `AWS_SECRET_ACCESS_KEY` | **Value**: Your new secret key

**Screenshot Guide:**
```
GitHub Repo → Settings → Secrets and Variables → Actions
┌─────────────────────────────────┐
│ Add Repository Secret           │
├─────────────────────────────────┤
│ Name: AWS_ACCESS_KEY_ID         │
│ Value: [Your New Access Key]    │
├─────────────────────────────────┤
│ Add Secret                      │
└─────────────────────────────────┘
```

#### Step 2: GitHub Actions Uses Secrets Safely

The updated `.github/workflows/cicd.yaml` now uses:

```yaml
- name: Configure DVC with AWS credentials
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  run: |
    dvc remote modify myremote access_key_id $AWS_ACCESS_KEY_ID
    dvc remote modify myremote secret_access_key $AWS_SECRET_ACCESS_KEY

- name: Pull data from DVC remote
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  run: |
    dvc pull -v
```

**Benefits:**
- ✅ Secrets never appear in logs
- ✅ Secrets only available during job execution
- ✅ Each repository has isolated secrets
- ✅ Secrets removed from GitHub logs automatically

---

## 📋 Alternative: Use IAM Role (Production Best Practice)

For production, use **AWS IAM Role for GitHub Actions**:

```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::ACCOUNT_ID:role/github-actions-role
    aws-region: us-east-1

- name: Pull data from DVC remote
  run: dvc pull -v
```

This eliminates the need for long-term credentials.

---

## 🔍 Verification Checklist

- [ ] AWS old access key revoked
- [ ] New AWS access key created
- [ ] `.dvc/config` added to `.gitignore`
- [ ] `AWS_ACCESS_KEY_ID` secret added to GitHub
- [ ] `AWS_SECRET_ACCESS_KEY` secret added to GitHub
- [ ] Local `.dvc/config.local` created with new credentials
- [ ] `dvc pull` works locally
- [ ] GitHub Actions passed with `DVC Pull` step succeeding
- [ ] `.dvc/config` file never shows credentials in logs

---

## 🚨 Security Best Practices

| ✅ DO | ❌ DON'T |
|------|---------|
| Use environment variables | Commit credentials in config files |
| Create IAM users for each service | Share AWS root account credentials |
| Rotate credentials regularly | Keep same credentials for years |
| Use GitHub Secrets for CI/CD | Hardcode secrets in code |
| Revoke compromised keys immediately | Ignore security warnings |
| Audit AWS access logs | Leave access keys unmonitored |

---

## 🆘 Troubleshooting

### Issue: "dvc pull" fails in CI/CD
```
Error: Access Denied to S3 bucket
```
**Solution:**
- Verify secrets are added to GitHub repository
- Check secret names: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
- Verify new access key has S3 permissions in AWS IAM

### Issue: Local "dvc pull" doesn't work
```
Error: NoCredentialsError
```
**Solution:**
```bash
# Verify environment variables are set
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY

# Or use config.local
dvc remote modify myremote access_key_id YOUR_KEY
dvc remote modify myremote secret_access_key YOUR_SECRET
```

### Issue: GitHub Actions logs show credentials
**Solution:**
- Never pass raw credentials to `echo` or `print` statements
- Use `${{ secrets.NAME }}` which GitHub automatically masks in logs
- Check for accidental logging in Python scripts

---

## 📚 References

- [DVC Remote Configuration](https://dvc.org/doc/user-guide/data-management/remote)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [DVC + AWS Integration](https://dvc.org/doc/user-guide/setup-analytics#using-aws-s3)
