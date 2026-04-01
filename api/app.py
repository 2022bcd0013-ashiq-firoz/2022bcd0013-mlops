from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import logging
from datetime import datetime
from pathlib import Path
import traceback

# ========================================
# LOGGING
# ========================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========================================
# FASTAPI INIT
# ========================================
app = FastAPI(
    title="MLOps Inference Endpoint",
    description="Inference API for ML model predictions",
    version="1.0.0"
)

# ========================================
# STUDENT INFO
# ========================================
STUDENT_NAME = "Ashiq Firoz"
ROLL_NUMBER = "2022BCD0013"

# ========================================
# PATHS (WORKS WITH YOUR STRUCTURE)
# ========================================
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "model.pkl"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"

# ========================================
# GLOBALS
# ========================================
model = None
scaler = None
EXPECTED_FEATURES = None


# ========================================
# LOAD MODEL
# ========================================
def load_model():
    global model, scaler, EXPECTED_FEATURES

    try:
        if MODEL_PATH.exists():
            model = joblib.load(MODEL_PATH)
            logger.info(f"Model loaded from {MODEL_PATH}")

            # Auto-detect feature size
            if hasattr(model, "n_features_in_"):
                EXPECTED_FEATURES = model.n_features_in_
                logger.info(f"Model expects {EXPECTED_FEATURES} features")
            else:
                EXPECTED_FEATURES = None
                logger.warning("Could not detect feature size from model")

        else:
            logger.error(f"Model not found at {MODEL_PATH}")
            model = None

        if SCALER_PATH.exists():
            scaler = joblib.load(SCALER_PATH)
            logger.info(f"Scaler loaded from {SCALER_PATH}")
        else:
            scaler = None
            logger.warning("Scaler not found, using raw features")

    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        model = None
        scaler = None


# ========================================
# STARTUP
# ========================================
@app.on_event("startup")
async def startup_event():
    load_model()
    logger.info("Application startup complete")


# ========================================
# REQUEST / RESPONSE MODELS
# ========================================
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    name: str
    roll_number: str
    message: str


class PredictionRequest(BaseModel):
    features: list


class PredictionResponse(BaseModel):
    prediction: float
    prediction_label: str
    name: str
    roll_number: str
    confidence: float = None
    timestamp: str


# ========================================
# HEALTH ENDPOINT
# ========================================
@app.get("/", response_model=HealthResponse)
@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        name=STUDENT_NAME,
        roll_number=ROLL_NUMBER,
        message="API is running successfully"
    )


# ========================================
# PREDICT ENDPOINT (FIXED)
# ========================================
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):

    try:
        if model is None:
            raise HTTPException(
                status_code=503,
                detail="Model not loaded"
            )

        # Convert input
        features = np.array(request.features)

        # 🔥 VALIDATION FIX
        if EXPECTED_FEATURES is not None:
            if features.shape[0] != EXPECTED_FEATURES:
                raise HTTPException(
                    status_code=400,
                    detail=f"Expected {EXPECTED_FEATURES} features, got {features.shape[0]}"
                )

        # Reshape for model
        features = features.reshape(1, -1)

        # Apply scaler if available
        if scaler is not None:
            try:
                features = scaler.transform(features)
            except Exception as e:
                logger.warning(f"Scaler failed: {str(e)}")

        # Prediction
        prediction = model.predict(features)[0]

        # Confidence (if available)
        confidence = None
        try:
            if hasattr(model, "predict_proba"):
                confidence = float(max(model.predict_proba(features)[0]))
        except:
            pass

        return PredictionResponse(
            prediction=float(prediction),
            prediction_label=_get_label(prediction),
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


# ========================================
# LABEL LOGIC
# ========================================
def _get_label(pred):
    if isinstance(pred, (int, float)):
        return "Positive" if pred >= 0.5 else "Negative"
    return str(pred)


# ========================================
# DEBUG ENDPOINT (VERY USEFUL)
# ========================================
@app.get("/debug")
def debug():
    return {
        "model_loaded": model is not None,
        "expected_features": EXPECTED_FEATURES,
        "model_path": str(MODEL_PATH),
        "exists": MODEL_PATH.exists()
    }


# ========================================
# MAIN
# ========================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)