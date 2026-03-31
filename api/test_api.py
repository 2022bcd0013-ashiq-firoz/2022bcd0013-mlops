"""
API Testing Guide and Examples
For MLOps Inference Endpoint

Run the API:
    python -m uvicorn api.app:app --reload --port 8000

Test endpoints as shown below.
"""

import requests
import json
from typing import List

BASE_URL = "http://localhost:8000"

# ==================== Health Check Tests ====================

def test_health_check():
    """Test health check endpoint"""
    print("\n=== Testing Health Check ===")
    
    # Test / endpoint
    response = requests.get(f"{BASE_URL}/")
    print(f"GET /")
    print(f"Status: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}\n")
    
    # Test /health endpoint
    response = requests.get(f"{BASE_URL}/health")
    print(f"GET /health")
    print(f"Status: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}\n")


# ==================== Model Status Tests ====================

def test_model_status():
    """Check if model is loaded"""
    print("\n=== Testing Model Status ===")
    response = requests.get(f"{BASE_URL}/model-status")
    print(f"GET /model-status")
    print(f"Status: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}\n")


# ==================== API Info ====================

def test_api_info():
    """Get API information"""
    print("\n=== API Information ===")
    response = requests.get(f"{BASE_URL}/info")
    print(f"GET /info")
    print(f"Status: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}\n")


# ==================== Single Prediction Test ====================

def test_single_prediction(features: List[float]):
    """
    Test single prediction endpoint
    
    Args:
        features: List of feature values
        
    Example:
        test_single_prediction([5.1, 3.5, 1.4, 0.2])
    """
    print("\n=== Testing Single Prediction ===")
    
    payload = {
        "features": features,
        "model_name": "default"
    }
    
    print(f"Sending prediction request with features: {features}")
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=payload
    )
    
    print(f"POST /predict")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nPrediction Result:")
        print(f"  Prediction: {result['prediction']}")
        print(f"  Label: {result['prediction_label']}")
        print(f"  Name: {result['name']}")
        print(f"  Roll Number: {result['roll_number']}")
        print(f"  Confidence: {result.get('confidence', 'N/A')}")
        print(f"  Timestamp: {result['timestamp']}\n")
    else:
        print(f"Error: {response.json()}\n")


# ==================== Batch Prediction Test ====================

def test_batch_prediction(samples: List[List[float]]):
    """
    Test batch prediction endpoint
    
    Args:
        samples: List of feature samples
        
    Example:
        test_batch_prediction([
            [5.1, 3.5, 1.4, 0.2],
            [6.2, 2.9, 4.3, 1.3],
            [7.1, 3.0, 5.9, 2.1]
        ])
    """
    print("\n=== Testing Batch Prediction ===")
    
    payload = {
        "samples": samples
    }
    
    print(f"Sending batch prediction request with {len(samples)} samples")
    
    response = requests.post(
        f"{BASE_URL}/predict-batch",
        json=payload
    )
    
    print(f"POST /predict-batch")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nBatch Prediction Result:")
        print(f"  Total Samples: {result['total_samples']}")
        print(f"  Predictions: {result['predictions']}")
        print(f"  Name: {result['name']}")
        print(f"  Roll Number: {result['roll_number']}")
        print(f"  Timestamp: {result['timestamp']}\n")
    else:
        print(f"Error: {response.json()}\n")


# ==================== Run All Tests ====================

if __name__ == "__main__":
    print("=" * 60)
    print("MLOps Inference Endpoint - Test Suite")
    print("=" * 60)
    
    try:
        # Run tests
        test_api_info()
        test_health_check()
        test_model_status()
        
        # Example predictions (adjust features based on your model)
        # For Iris dataset: [sepal_length, sepal_width, petal_length, petal_width]
        test_single_prediction([5.1, 3.5, 1.4, 0.2])
        
        # Batch prediction
        test_batch_prediction([
            [5.1, 3.5, 1.4, 0.2],
            [6.2, 2.9, 4.3, 1.3],
            [7.1, 3.0, 5.9, 2.1]
        ])
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error: Make sure the API is running!")
        print("   Run: python -m uvicorn api.app:app --reload --port 8000")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Interactive Testing:")
    print("- Swagger UI: http://localhost:8000/docs")
    print("- ReDoc: http://localhost:8000/redoc")
    print("=" * 60)
