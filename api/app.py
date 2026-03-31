from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import logging
from datetime import datetime
from pathlib import Path
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MLOps Inference Endpoint",
    description="Inference API for ML model predictions",
    version="1.0.0"
)

# Student Information
STUDENT_NAME = "Ashiq Firoz"
ROLL_NUMBER = "2022BCD0013"

# Model paths
MODEL_PATH = Path(__file__).parent.parent / "models" / "model.pkl"
SCALER_PATH = Path(__file__).parent.parent / "models" / "scaler.pkl"

# Global model variables
model = None
scaler = None


def load_model():
    """Load trained model and scaler from disk"""
    global model, scaler
    try:
        if MODEL_PATH.exists():
            model = joblib.load(MODEL_PATH)
            logger.info(f"Model loaded from {MODEL_PATH}")
        else:
            logger.warning(f"Model not found at {MODEL_PATH}. Using None.")
            model = None
            
        if SCALER_PATH.exists():
            scaler = joblib.load(SCALER_PATH)
            logger.info(f"Scaler loaded from {SCALER_PATH}")
        else:
            logger.warning(f"Scaler not found at {SCALER_PATH}. Using None.")
            scaler = None
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        model = None
        scaler = None


# Load model on startup
@app.on_event("startup")
async def startup_event():
    """Load model when application starts"""
    load_model()
    logger.info("Application startup complete")


# ==================== Request/Response Models ====================

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: str
    name: str
    roll_number: str
    message: str


class PredictionRequest(BaseModel):
    """Input features for prediction"""
    features: list
    model_name: str = "default"


class PredictionResponse(BaseModel):
    """Prediction response model"""
    prediction: float
    prediction_label: str
    name: str
    roll_number: str
    confidence: float = None
    timestamp: str


class ModelStatusResponse(BaseModel):
    """Model status response"""
    model_loaded: bool
    scaler_loaded: bool
    model_path: str
    scaler_path: str


# ==================== Health Check Endpoints ====================

@app.get("/", response_model=HealthResponse, tags=["Health"])
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint - verifies API is running
    
    Returns:
        HealthResponse: Status and student information
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        name=STUDENT_NAME,
        roll_number=ROLL_NUMBER,
        message="API is running successfully"
    )


@app.get("/model-status", response_model=ModelStatusResponse, tags=["Health"])
async def model_status():
    """
    Check if model and scaler are loaded
    
    Returns:
        ModelStatusResponse: Status of model components
    """
    return ModelStatusResponse(
        model_loaded=model is not None,
        scaler_loaded=scaler is not None,
        model_path=str(MODEL_PATH),
        scaler_path=str(SCALER_PATH)
    )


# ==================== Prediction Endpoint ====================

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(request: PredictionRequest):
    """
    Make prediction on input features
    
    Args:
        request: PredictionRequest with features list
        
    Returns:
        PredictionResponse: Prediction result with metadata
        
    Raises:
        HTTPException: If model is not loaded or prediction fails
    """
    try:
        if model is None:
            raise HTTPException(
                status_code=503,
                detail="Model not loaded. Please check model file."
            )
        
        # Convert features to numpy array
        features = np.array(request.features).reshape(1, -1)
        
        # Scale features if scaler is available
        if scaler is not None:
            try:
                features = scaler.transform(features)
            except Exception as e:
                logger.warning(f"Scaler transform failed: {str(e)}. Using raw features.")
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        # Get prediction probability if available (for classification models)
        confidence = None
        try:
            if hasattr(model, 'predict_proba'):
                probabilities = model.predict_proba(features)[0]
                confidence = float(max(probabilities))
            elif hasattr(model, 'decision_function'):
                confidence = float(model.decision_function(features)[0])
        except Exception as e:
            logger.debug(f"Could not compute confidence: {str(e)}")
        
        # Determine prediction label based on model type
        prediction_label = _get_prediction_label(prediction)
        
        return PredictionResponse(
            prediction=float(prediction),
            prediction_label=prediction_label,
            name=STUDENT_NAME,
            roll_number=ROLL_NUMBER,
            confidence=confidence,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


def _get_prediction_label(prediction: float) -> str:
    """
    Convert numeric prediction to label
    
    Args:
        prediction: Numeric prediction value
        
    Returns:
        str: Prediction label
    """
    # Adjust this logic based on your model type
    if isinstance(prediction, (int, float)):
        if prediction >= 0.5:
            return "Positive" if prediction <= 1.0 else f"Class_{int(prediction)}"
        else:
            return "Negative" if prediction <= 1.0 else f"Class_{int(prediction)}"
    return str(prediction)


# ==================== Batch Prediction Endpoint ====================

class BatchPredictionRequest(BaseModel):
    """Batch prediction request"""
    samples: list


class BatchPredictionResponse(BaseModel):
    """Batch prediction response"""
    predictions: list
    name: str
    roll_number: str
    timestamp: str
    total_samples: int


@app.post("/predict-batch", response_model=BatchPredictionResponse, tags=["Prediction"])
async def predict_batch(request: BatchPredictionRequest):
    """
    Make predictions on multiple samples
    
    Args:
        request: BatchPredictionRequest with list of feature samples
        
    Returns:
        BatchPredictionResponse: List of predictions with metadata
        
    Raises:
        HTTPException: If model is not loaded or prediction fails
    """
    try:
        if model is None:
            raise HTTPException(
                status_code=503,
                detail="Model not loaded. Please check model file."
            )
        
        # Convert to numpy array
        features = np.array(request.samples)
        
        # Scale if scaler available
        if scaler is not None:
            try:
                features = scaler.transform(features)
            except Exception as e:
                logger.warning(f"Scaler transform failed: {str(e)}. Using raw features.")
        
        # Make predictions
        predictions = model.predict(features)
        
        return BatchPredictionResponse(
            predictions=predictions.tolist(),
            name=STUDENT_NAME,
            roll_number=ROLL_NUMBER,
            timestamp=datetime.now().isoformat(),
            total_samples=len(predictions)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction failed: {str(e)}"
        )


# ==================== Root Endpoint ====================

@app.get("/info", tags=["Info"])
async def info():
    """Get API information"""
    return {
        "api_name": "MLOps Inference Endpoint",
        "version": "1.0.0",
        "developer": STUDENT_NAME,
        "roll_number": ROLL_NUMBER,
        "endpoints": {
            "health": "/health or /",
            "predict": "/predict (POST)",
            "batch_predict": "/predict-batch (POST)",
            "model_status": "/model-status",
            "docs": "/docs (Swagger UI)",
            "redoc": "/redoc"
        }
    }


# ==================== Error Handlers ====================

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions"""
    logger.error(f"ValueError: {str(exc)}")
    return {
        "detail": str(exc),
        "name": STUDENT_NAME,
        "roll_number": ROLL_NUMBER
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
