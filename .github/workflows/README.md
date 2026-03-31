# MLOps CI/CD Pipeline Documentation

## Overview

This CI/CD pipeline automates the complete machine learning workflow, including data versioning, model training, and experiment tracking.

## Pipeline Stages

### 1. **Code Checkout**
- Uses `actions/checkout@v4` to pull the latest code
- Fetches full git history for DVC compatibility

### 2. **Environment Setup**
- Sets up Python 3.11 environment
- Caches pip dependencies for faster builds
- Installs `uv` package manager

### 3. **Dependency Installation**
- Installs all required packages:
  - **Data Processing**: `pandas`, `numpy`
  - **ML Libraries**: `scikit-learn`, `xgboost`
  - **Experiment Tracking**: `mlflow`
  - **Data Versioning**: `dvc`, `dvc-s3`

### 4. **DVC Data Pull**
- Initializes DVC configuration
- Pulls data from remote DVC storage (if configured)
- Falls back to creating dummy data for CI testing if needed
- Validates data file existence

### 5. **MLflow Setup & Training**
- Starts MLflow server on `localhost:8080`
- Trains base model with default hyperparameters
- Trains tuned model with optimized hyperparameters
- Logs all parameters and metrics to MLflow

### 6. **Metrics Generation**
- Queries MLflow API for all experiments and runs
- Collects parameters, metrics, and model information
- Generates detailed metrics report
- Saves report as artifact

### 7. **Testing & Validation**
- Validates data file integrity
- Verifies MLflow runs directory
- Performs sanity checks

### 8. **Artifact Upload**
- Uploads metrics report as GitHub artifact
- Retains for 30 days
- Available for download from Actions tab

## Trigger Events

The pipeline runs on:
- **Push events** to `main` and `develop` branches
- **Pull requests** to `main` branch
- **Daily schedule** at 00:00 UTC (for continuous training)
- **Manual trigger** via `workflow_dispatch`

## Configuration

### MLflow
The pipeline assumes MLflow is already running on `localhost:8080`. To configure remote MLflow:

```bash
export MLFLOW_TRACKING_URI=<your-remote-uri>
```

### DVC Remote
To use DVC remote storage:

```bash
dvc remote add -d myremote s3://my-bucket/path
dvc remote modify myremote --local access_key_id <KEY>
dvc remote modify myremote --local secret_access_key <SECRET>
```

### GitHub Secrets (Optional)
If using remote storage, add these secrets to your GitHub repository:
- `DVC_REMOTE_URL`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

## Output Artifacts

- **metrics_report.json**: Complete MLflow metrics and parameters in JSON format
- Available for 30 days after workflow run

## Monitoring

1. **GitHub Actions**: View real-time logs in the Actions tab
2. **MLflow UI**: Access at `http://localhost:8080` during pipeline execution
3. **Artifacts**: Download metrics reports from workflow summary

## Troubleshooting

### Issue: "data/data.csv not found"
**Solution**: DVC pull failed or remote not configured
- Check DVC remote configuration: `dvc remote list`
- Ensure credentials are configured
- Pipeline will create dummy data for CI if needed

### Issue: "MLflow server not responding"
**Solution**: Server startup failed
- Check port 8080 is available
- Verify MLflow installation: `pip install mlflow`
- Review workflow logs for details

### Issue: "Cannot connect to DVC remote"
**Solution**: Credentials or configuration missing
- Configure DVC remote: `dvc remote add -d myremote <url>`
- Add credentials to GitHub Secrets
- Update workflow file with secret references

## Local Testing

To test the pipeline locally:

```bash
# 1. Install dependencies
uv pip install pandas numpy scikit-learn xgboost mlflow dvc

# 2. Start MLflow server
mlflow server --host 0.0.0.0 --port 8080 &

# 3. Pull data (if configured)
dvc pull

# 4. Run training
export MLFLOW_TRACKING_URI=http://localhost:8080
python src/train.py --data_path data/data.csv --run_type base

# 5. View experiments
# Open http://localhost:8080 in your browser
```

## Pipeline Flow Diagram

```
Code Checkout
    ↓
Setup Python Environment
    ↓
Install Dependencies
    ↓
Setup DVC & Pull Data
    ↓
Start MLflow Server
    ↓
┌─────────────────────┐
│ Train Base Model    │
│ Train Tuned Model   │  (parallel-capable)
└─────────────────────┘
    ↓
Query MLflow Metrics
    ↓
Generate Metrics Report
    ↓
Upload Artifacts
    ↓
Pipeline Complete ✓
```

## Next Steps

1. Configure DVC remote for production data
2. Set up MLflow remote tracking server
3. Add GitHub Secrets for remote credentials
4. Customize hyperparameters in `src/train.py`
5. Add additional metrics/logging as needed
