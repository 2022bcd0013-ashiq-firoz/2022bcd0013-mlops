# 🔒 DVC + S3 Credential Options (Comparison)

## Option 1: GitHub Secrets + Environment Variables ⭐ (RECOMMENDED)

### How It Works
```
GitHub Actions Workflow
    ↓
Environment Variables (GitHub Secrets injected)
    ↓
DVC reads AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY from ENV
    ↓
Pulls data from S3
```

### Setup (5 minutes)
```bash
# 1. Add to GitHub Secrets
# AWS_ACCESS_KEY_ID = AKIA...
# AWS_SECRET_ACCESS_KEY = ...

# 2. Workflow automatically receives them
env:
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

# 3. DVC auto-detects and uses them
dvc pull
```

### Pros ✅
- Simple and straightforward
- Secrets masked in logs automatically
- Works with any AWS account
- No additional infrastructure
- Can rotate credentials anytime

### Cons ❌
- Long-term credentials (not ideal for production)
- Requires manual credential rotation
- Credentials stored in GitHub (encrypted at rest)

### Security Level
⭐⭐⭐ Good for development/CI - Acceptable for production

---

## Option 2: AWS IAM Role (Production Best Practice) 🏆

### How It Works
```
GitHub Actions Workflow
    ↓
AWS OIDC Trust Relationship
    ↓
Assume IAM Role (temporary credentials)
    ↓
DVC uses temporary credentials
    ↓
Updates every 1 hour automatically
```

### Setup (15 minutes - One time)
```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::ACCOUNT_ID:role/github-actions-role
    aws-region: us-east-1

- name: DVC Pull
  run: dvc pull
```

### Pros ✅
- **No long-term credentials** (credentials auto-rotate every hour)
- Maximum security for production
- No secret rotation needed
- Audit trail in AWS CloudTrail
- Follows AWS best practices
- Fine-grained IAM permission control

### Cons ❌
- Requires AWS account setup (one-time)
- More complex initial setup
- Requires IAM permissions to create role
- Not available for free AWS tier

### Security Level
⭐⭐⭐⭐⭐ Best for production environments

### Setup Guide
1. Create OIDC Provider in AWS
2. Create IAM Role with S3 permissions
3. Add trust relationship for GitHub
4. Reference role in workflow

---

## Option 3: .dvc/config.local (Local Development Only)

### How It Works
```
Local Machine
    ↓
.dvc/config.local stores credentials
    ↓
.gitignore prevents commit
    ↓
dvc pull works locally
```

### Setup (2 minutes)
```bash
cat > .dvc/config.local << EOF
['remote "myremote"']
    url = s3://2022bcd0013-mlops/mlops-assignment
    access_key_id = AKIA...
    secret_access_key = ...
EOF

dvc pull
```

### Pros ✅
- Works offline
- No GitHub secrets needed
- Credentials stay on your machine
- Simple setup

### Cons ❌
- ⚠️ NOT for CI/CD
- Credentials on disk (if compromised)
- Manual credential management
- Doesn't help with GitHub Actions

### Security Level
⭐⭐ Good for local development ONLY

---

## Option 4: Temporary Credentials (AWS STS)

### How It Works
```
GitHub Actions
    ↓
Request temporary credentials from STS
    ↓
Use temporary credentials (1 hour expiry)
    ↓
Auto-cleanup on expiry
```

### Setup Code
```bash
# Generate temporary credentials
aws sts get-session-token --duration-seconds 3600

# Use in GitHub Actions
export AWS_ACCESS_KEY_ID=$TEMP_KEY
export AWS_SECRET_ACCESS_KEY=$TEMP_SECRET
export AWS_SESSION_TOKEN=$SESSION_TOKEN

dvc pull
```

### Pros ✅
- Temporary (auto-expires)
- No rotation needed
- Good compromise

### Cons ❌
- More complex setup
- Requires base credentials to generate temp ones
- Still uses long-term credentials as base

### Security Level
⭐⭐⭐ Better than long-term, but IAM Role is superior

---

## Recommended Setup Path

### For Learning/Development
```
Use Option 1: GitHub Secrets + Environment Variables
├─ Quick to setup (5 minutes)
├─ Good enough for assignments
├─ Easy to rotate credentials
└─ Perfect for learning CI/CD
```

### For Production
```
Use Option 2: AWS IAM Role (OIDC)
├─ No long-term credentials
├─ Auto-rotating temporary credentials
├─ Meets compliance requirements
└─ Production-grade security
```

---

## Current Implementation

Your setup uses **Option 1** (GitHub Secrets), which is appropriate for:
- ✅ Course assignments
- ✅ Development/testing
- ✅ Teams with small credential rotation cycle
- ✅ Learning CI/CD concepts

---

## Migration Path

```
Week 1: Implement Option 1 (GitHub Secrets)
    ↓
Week 2-4: Learn and test
    ↓
Week 5+: Consider Option 2 (IAM Role) for production
```

---

## Quick Comparison Table

| Aspect | Option 1 | Option 2 | Option 3 | Option 4 |
|--------|----------|----------|----------|----------|
| **Setup Time** | 5 min | 15 min | 2 min | 10 min |
| **Security** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Rotation** | Manual | Auto | Manual | N/A |
| **CI/CD** | ✅ | ✅ | ❌ | ✅ |
| **Complexity** | Simple | Complex | Simple | Medium |
| **Production** | OK | Best | No | Good |
| **Cost** | Free | Free | Free | Free* |

---

## Environment Variable Reference

DVC automatically reads these from environment:

```bash
# S3 Authentication
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...

# Optional
export AWS_DEFAULT_REGION=us-east-1
export AWS_SESSION_TOKEN=...  # For temporary credentials
```

---

## Next Steps

1. **Implement Option 1** (GitHub Secrets) now
2. **Test locally** with setup scripts
3. **Verify CI/CD** passes
4. **Later**: Research Option 2 if moving to production Azure

See `GITHUB_SECRETS_SETUP.md` for step-by-step instructions.
