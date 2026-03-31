# CI/CD Pipeline Quick Start Guide

## 📋 Checklist Before First Run

- [ ] Ensure `src/train.py` is properly configured
- [ ] Ensure MLflow is accessible or will be started by pipeline
- [ ] Create `data/data.csv` or configure DVC remote
- [ ] Push code to `main` or `develop` branch
- [ ] Check GitHub Actions tab for workflow runs

## 🚀 What the Pipeline Does

```
When you push code to main/develop or open a PR:

1️⃣  Checks out your code
2️⃣  Sets up Python 3.11 environment
3️⃣  Installs: pandas, numpy, scikit-learn, xgboost, mlflow, dvc
4️⃣  Pulls data from DVC (or uses local)
5️⃣  Starts MLflow server on localhost:8080
6️⃣  Trains base model → Logs to MLflow
7️⃣  Trains tuned model → Logs to MLflow
8️⃣  Generates metrics report
9️⃣  Uploads metrics as artifact
```

## 📊 Key Endpoints

| Component | URL/Location |
|-----------|-------------|
| GitHub Actions | Settings → Actions |
| MLflow UI (local run) | `http://localhost:8080` |
| Metrics Artifact | Actions → Run → Artifacts |
| Workflow Logs | Actions → Run → Logs |

## 🔧 Configuration

### Required: Ensure `src/train.py` can accept these arguments
```bash
python src/train.py --data_path data/data.csv --run_type base
```

### Optional: Configure DVC Remote
```bash
dvc remote add -d myremote s3://bucket/path
dvc push
```

### Optional: Configure MLflow Remote
```bash
export MLFLOW_TRACKING_URI=http://your-mlflow-server:5000
```

## 📝 Monitoring Pipeline Runs

1. **Go to GitHub Actions tab**
2. **Click on latest workflow run**
3. **View step logs in real-time**
4. **Download artifacts** after completion

## 🆘 Troubleshooting

### ❌ Pipeline Failed: "data/data.csv not found"
✅ **Fix**: Create dummy data or configure DVC:
```bash
dvc remote add -d myremote <url>
dvc push
```

### ❌ Pipeline Failed: "MLflow server not responding"
✅ **Fix**: Verify MLflow installation:
```bash
pip install mlflow
```

### ❌ Pipeline Failed: "Cannot import module"
✅ **Fix**: Ensure all dependencies are in pyproject.toml:
```bash
python -m pip install -e .
```

## 🎯 Common Tasks

### Add a new dependency
1. Edit `pyproject.toml`
2. Add to `dependencies = [...]`
3. Commit and push

### Change training parameters
1. Edit `src/train.py`
2. Modify model initialization
3. Commit and push

### Add custom metrics
1. Edit `src/train.py`
2. Add `mlflow.log_metric("name", value)`
3. Commit and push

### Schedule daily training
✅ Already configured! Runs daily at 00:00 UTC

### Manually trigger pipeline
1. Go to GitHub Actions
2. Click "MLOps CI/CD Pipeline"
3. Click "Run workflow"

## 📊 Viewing Results

### Via Metrics Artifact
```bash
# Download metrics_report.json from GitHub Actions
# View with any JSON viewer
```

### Via MLflow UI
```bash
# During pipeline run (GitHub Actions provides access)
# Or locally after running src/train.py
http://localhost:8080
```

## 🔄 Pipeline Workflow

```
┌─────────────────┐
│   Code Push     │
│ (main/develop)  │
└────────┬────────┘
         │
         ▼
┌──────────────────────────┐
│ GitHub Actions Triggered │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Setup Python + Install   │
│       Dependencies       │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│   DVC Pull Data          │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  Run Training Script     │
│  + MLflow Logging        │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Generate Metrics Report  │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  Upload Artifacts        │
│  + Workflow Summary      │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│   ✓ Pipeline Complete    │
│   View results in        │
│   GitHub Actions         │
└──────────────────────────┘
```

## 📚 More Information

- Full documentation: See `.github/workflows/README.md`
- DVC setup guide: See `DVC_SETUP.md`
- Training script: See `src/train.py`
- Project config: See `pyproject.toml`

## 💡 Tips

- **Run locally first**: Test your training script locally before pushing
- **Check logs carefully**: GitHub Actions logs show exactly what failed
- **Download artifacts**: Always download metrics reports for analysis
- **Monitor MLflow**: Watch MLflow UI to see experiments in real-time
