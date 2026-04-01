# MLOps Assignment - Model Training Pipeline

A complete machine learning operations (MLOps) project demonstrating best practices in model development, versioning, tracking, and deployment. This project implements a classification pipeline using XGBoost to predict customer churn, with integrated data versioning (DVC), experiment tracking (MLflow), and a FastAPI inference endpoint.

## Overview

This project showcases:
- Data versioning and management using DVC
- Experiment tracking and model comparison with MLflow
- Model training with hyperparameter optimization
- FastAPI-based inference endpoint for predictions
- Docker containerization for reproducible deployments
- Comprehensive testing and code quality checks

## Project Structure

```
.
├── api/               # FastAPI application
│   ├── app.py        # Main inference endpoint
│   └── test_api.py   # API tests
├── data/             # Dataset management
│   ├── data.csv      # Original dataset
│   ├── data_v2.csv   # Updated dataset
│   └── *.dvc         # DVC data versioning files
├── models/           # Trained model artifacts
├── src/              # Training pipeline source code
│   ├── main.py       # Entry point
│   ├── train.py      # Model training script
├── mlruns/           # MLflow experiment tracking storage
├── pyproject.toml    # Project dependencies and metadata
├── Dockerfile        # Container configuration
└── Readme.md         # This file
```

## Prerequisites

- Python 3.11 or higher
- pip or uv package manager
- Docker (optional, for containerization)

## Environment Setup

Install dependencies using uv:

```bash
uv install
```

Or using pip:

```bash
pip install -e ".[dev]"
```

## Dataset

The project uses customer churn data (v2):
- File: `data/data_v2.csv`
- DVC tracking: Version-controlled through `data_v2.csv.dvc`
- Target variable: Churn (Yes/No)
- Features: Customer demographics and service usage

## Model Training

Train the XGBoost model using the training pipeline:

```bash
python src/train.py --data_path data/data_v2.csv --run_type base
```

Parameters:
- `--data_path`: Path to the training dataset (default: `data/data_v2.csv`)
- `--run_type`: Type of run - `base` for baseline or `tuned` for hyperparameter-tuned model

The training process:
1. Loads and preprocesses the dataset
2. Encodes categorical features
3. Splits data into train/test sets
4. Trains XGBoost classifier
5. Logs metrics (accuracy, F1-score) to MLflow
6. Saves model artifacts

## Experiment Tracking

MLflow tracks all model experiments and runs:

```bash
mlflow ui
```

Access the UI at `http://localhost:5000` to view:
- Experiment history
- Model metrics (accuracy, F1-score)
- Parameters used
- Model artifacts

## Inference API

The FastAPI application provides a prediction endpoint:

```bash
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

Access the API at `http://localhost:8000`:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### API Endpoints

**GET** `/health`: Health check endpoint
- Returns: `{"status": "OK"}`

**POST** `/predict`: Make predictions on customer data
- Requires: JSON payload with customer features
- Returns: `{"prediction": 0 or 1, "probability": float}`

For full API documentation, see [api/API_DOCUMENTATION.md](api/API_DOCUMENTATION.md)

## Testing

Run API tests:

```bash
pytest api/test_api.py -v
```

Run tests with coverage:

```bash
pytest --cov=api --cov-report=html
```

## Docker

Build and run the application in a container:

```bash
# Build the image
docker build -t mlops-assignment .

# Run the container
docker run -p 8000:8000 mlops-assignment
```

## Data Versioning

Track dataset changes using DVC:

```bash
# Pull data from remote storage (if configured)
dvc pull

# Push versioned data
dvc push

# Check data status
dvc status
```

## Dependencies

Key packages:
- `scikit-learn`: Machine learning algorithms
- `xgboost`: Gradient boosting classifier
- `pandas`: Data manipulation
- `numpy`: Numerical computations
- `mlflow`: Experiment tracking
- `dvc`: Data versioning
- `fastapi`: Web API framework
- `pydantic`: Data validation
- `joblib`: Model serialization



## Workflow

1. Prepare and version data with DVC
2. Train models using `train.py` with parameter variations
3. Compare experiments in MLflow UI
4. Select best model for deployment
5. Deploy inference endpoint with FastAPI
6. Serve predictions via Docker

## Notes

- Model training logs are automatically saved to MLflow
- Experiment tracking helps compare different model configurations
- The inference API expects preprocessed features in the same format as training data
- Scaler and model are loaded at API startup for performance
