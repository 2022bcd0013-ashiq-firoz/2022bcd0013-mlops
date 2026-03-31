@echo off
REM setup-dvc-local.bat - Configure DVC with AWS credentials for local development (Windows)

echo 🔐 Configuring DVC with AWS credentials...

REM Check if credentials are set in environment
if "%AWS_ACCESS_KEY_ID%"=="" (
    echo ❌ Error: AWS_ACCESS_KEY_ID not found in environment variables
    echo.
    echo Please set environment variables:
    echo   set AWS_ACCESS_KEY_ID=your_access_key
    echo   set AWS_SECRET_ACCESS_KEY=your_secret_key
    exit /b 1
)

if "%AWS_SECRET_ACCESS_KEY%"=="" (
    echo ❌ Error: AWS_SECRET_ACCESS_KEY not found in environment variables
    exit /b 1
)

REM Create .dvc/config.local with credentials (Git ignores this)
(
    echo ['remote "myremote"']
    echo     url = s3://2022bcd0013-mlops/mlops-assignment
    echo     access_key_id = %AWS_ACCESS_KEY_ID%
    echo     secret_access_key = %AWS_SECRET_ACCESS_KEY%
) > .dvc\config.local

echo ✅ DVC configured with credentials in .dvc\config.local
echo ℹ️  This file is in .gitignore and won't be committed
echo.
echo Next steps:
echo   dvc pull          - Pull data from S3
echo   python src/train.py - Train model
