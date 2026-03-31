# DVC Configuration Guide

## Local Configuration
This file shows example DVC configurations for different remote storage options.

### AWS S3 Remote (Recommended)
```
[remote "myremote"]
    url = s3://my-bucket/dvc-storage
    access_key_id = <your-key>
    secret_access_key = <your-secret>
```

### Azure Blob Storage
```
[remote "myremote"]
    url = azure://my-container/dvc-storage
    connection_string = <your-connection-string>
```

### Google Cloud Storage
```
[remote "myremote"]
    url = gs://my-bucket/dvc-storage
    projectname = <your-project>
```

### Local Directory
```
[remote "myremote"]
    url = /mnt/shared/dvc-storage
```

## Setup Instructions

### 1. Initialize DVC (if not already done)
```bash
cd d:\IIITK\mlops\assignment
dvc init
```

### 2. Add Remote
```bash
# For S3
dvc remote add -d myremote s3://my-bucket/dvc-storage

# Or set default
dvc remote default myremote
```

### 3. Configure Credentials
```bash
dvc remote modify myremote --local access_key_id <YOUR_KEY>
dvc remote modify myremote --local secret_access_key <YOUR_SECRET>
```

### 4. Push Data to Remote
```bash
dvc push
```

### 5. Verify Configuration
```bash
dvc remote list
dvc config --list
```

## For GitHub Actions

Add these secrets to your GitHub repository:
1. Go to Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `DVC_REMOTE_AWS_KEY` - Your AWS access key
   - `DVC_REMOTE_AWS_SECRET` - Your AWS secret key

Update the workflow to use:
```yaml
env:
  AWS_ACCESS_KEY_ID: ${{ secrets.DVC_REMOTE_AWS_KEY }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.DVC_REMOTE_AWS_SECRET }}
```
