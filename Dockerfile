# ========================================
# BASE IMAGE
# ========================================
FROM python:3.11-slim

# ========================================
# SET WORKING DIRECTORY
# ========================================
WORKDIR /app

# ========================================
# COPY PROJECT FILES
# ========================================
COPY api ./api
COPY src ./src
COPY models ./models
COPY data ./data
COPY pyproject.toml .

# ========================================
# INSTALL DEPENDENCIES
# ========================================
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        fastapi \
        uvicorn \
        numpy \
        pandas \
        scikit-learn \
        xgboost \
        joblib \
        mlflow \
        dvc

# ========================================
# EXPOSE PORT
# ========================================
EXPOSE 8000

# ========================================
# RUN APPLICATION
# ========================================
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]