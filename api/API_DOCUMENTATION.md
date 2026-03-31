# MLOps Inference Endpoint API Documentation

## Overview

FastAPI-based inference endpoint for ML model predictions with built-in health checks and batch processing support.

**Developer:** Ashiq Firoz  
**Roll Number:** 2022BCD0013

---

## Quick Start

### 1. Install Dependencies
```bash
# Using pip
pip install fastapi uvicorn pydantic joblib

# Using uv
uv pip install fastapi uvicorn pydantic joblib
```

### 2. Run the API
```bash
# Development mode with auto-reload
python -m uvicorn api.app:app --reload --port 8000

# Production mode
python -m uvicorn api.app:app --host 0.0.0.0 --port 8000 --workers 4
```

### 3. Access Interactive Documentation
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## API Endpoints

### 1. Health Check Endpoints

#### GET `/` or `/health`
**Description:** Health check - verifies API is running  
**Response:** 200 OK

```json
{
  "status": "healthy",
  "timestamp": "2024-03-31T10:30:45.123456",
  "name": "Ashiq Firoz",
  "roll_number": "2022BCD0013",
  "message": "API is running successfully"
}
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/health"
```

---

### 2. Prediction Endpoint

#### POST `/predict`
**Description:** Make prediction on single sample  
**Request Body:**
```json
{
  "features": [5.1, 3.5, 1.4, 0.2],
  "model_name": "default"
}
```

**Response:** 200 OK
```json
{
  "prediction": 0.0,
  "prediction_label": "Negative",
  "name": "Ashiq Firoz",
  "roll_number": "2022BCD0013",
  "confidence": 0.95,
  "timestamp": "2024-03-31T10:30:45.123456"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2], "model_name": "default"}'
```

**Python Example:**
```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={
        "features": [5.1, 3.5, 1.4, 0.2],
        "model_name": "default"
    }
)
print(response.json())
```

---

### 3. Batch Prediction Endpoint

#### POST `/predict-batch`
**Description:** Make predictions on multiple samples  
**Request Body:**
```json
{
  "samples": [
    [5.1, 3.5, 1.4, 0.2],
    [6.2, 2.9, 4.3, 1.3],
    [7.1, 3.0, 5.9, 2.1]
  ]
}
```

**Response:** 200 OK
```json
{
  "predictions": [0.0, 1.0, 2.0],
  "name": "Ashiq Firoz",
  "roll_number": "2022BCD0013",
  "timestamp": "2024-03-31T10:30:45.123456",
  "total_samples": 3
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/predict-batch" \
  -H "Content-Type: application/json" \
  -d '{
    "samples": [
      [5.1, 3.5, 1.4, 0.2],
      [6.2, 2.9, 4.3, 1.3],
      [7.1, 3.0, 5.9, 2.1]
    ]
  }'
```

---

### 4. Model Status Endpoint

#### GET `/model-status`
**Description:** Check if model and scaler are loaded  
**Response:** 200 OK

```json
{
  "model_loaded": true,
  "scaler_loaded": true,
  "model_path": "d:\\IIITK\\mlops\\assignment\\models\\model.pkl",
  "scaler_path": "d:\\IIITK\\mlops\\assignment\\models\\scaler.pkl"
}
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/model-status"
```

---

### 5. API Information Endpoint

#### GET `/info`
**Description:** Get API endpoints and metadata  
**Response:** 200 OK

```json
{
  "api_name": "MLOps Inference Endpoint",
  "version": "1.0.0",
  "developer": "Ashiq Firoz",
  "roll_number": "2022BCD0013",
  "endpoints": {
    "health": "/health or /",
    "predict": "/predict (POST)",
    "batch_predict": "/predict-batch (POST)",
    "model_status": "/model-status",
    "docs": "/docs (Swagger UI)",
    "redoc": "/redoc"
  }
}
```

---

## Model Setup

### Expected Directory Structure
```
assignment/
├── api/
│   ├── app.py                 # Main API application
│   └── test_api.py            # Test script
├── models/
│   ├── model.pkl              # Trained model (required)
│   └── scaler.pkl             # Feature scaler (optional)
├── pyproject.toml
└── README.md
```

### Preparing Model Files

1. **Train your model** and save with joblib:
```python
import joblib
from sklearn.preprocessing import StandardScaler

# After training
joblib.dump(model, "models/model.pkl")
joblib.dump(scaler, "models/scaler.pkl")
```

2. **Create models directory:**
```bash
mkdir models
```

3. **Place model files:**
```bash
# Move trained model and scaler to models/
cp /path/to/model.pkl models/
cp /path/to/scaler.pkl models/
```

---

## Error Responses

### Model Not Loaded (Error Code: 503)
```json
{
  "detail": "Model not loaded. Please check model file."
}
```
**Solution:** Ensure model.pkl exists in the `models/` directory

### Invalid Features (Error Code: 422)
```json
{
  "detail": "Invalid input - features must be a list of numbers"
}
```
**Solution:** Ensure features are provided as a list of floats/ints

### Server Error (Error Code: 500)
```json
{
  "detail": "Prediction failed: [error details]"
}
```
**Solution:** Check API logs for detailed error information

---

## Testing

### Run Test Suite
```bash
python api/test_api.py
```

### Manual Testing via Swagger UI
1. Open http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Enter sample data
5. Click "Execute"

### Example Test with cURL
```bash
# Health check
curl http://localhost:8000/health

# Single prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'

# Batch prediction
curl -X POST http://localhost:8000/predict-batch \
  -H "Content-Type: application/json" \
  -d '{"samples": [[5.1, 3.5, 1.4, 0.2], [6.2, 2.9, 4.3, 1.3]]}'
```

---

## Logging & Debugging

### View Application Logs
```bash
# With development mode
python -m uvicorn api.app:app --reload --log-level debug

# Production mode with logs
python -m uvicorn api.app:app --log-level info > api.log 2>&1
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Port 8000 already in use | Use `--port 8001` or kill process on 8000 |
| Model not found | Check `models/` directory and file names |
| Import errors | Run `pip install -r requirements.txt` |
| Scaler mismatch | Scaler defaults to None if not available; optional |

---

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.app:app --bind 0.0.0.0:8000
```

### Using Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install -e .
COPY . .
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Response Schema

All responses include:
- **name:** "Ashiq Firoz" (Student name)
- **roll_number:** "2022BCD0013" (Roll number)
- **timestamp:** ISO 8601 formatted timestamp
- **Additional fields:** Specific to each endpoint

---

## Notes

- Model loading happens at application startup
- Scaler is optional; API works without it (warnings logged)
- All responses include student information as required
- Feature scaling is automatic if scaler is available
- Confidence scores available for classification models
