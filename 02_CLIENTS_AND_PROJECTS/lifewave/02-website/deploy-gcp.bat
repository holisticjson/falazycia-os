@echo off
:: Premium GCP Cloud Run Deployment script for Jaison X2O Portal
:: Designed by Jaison AI Engineering

set PROJECT_ID=holistic-dashboard-dev
set SERVICE_NAME=jaison-x2o-portal
set REGION=europe-west1

echo ==========================================================
echo 🚀 DEPLOYING JAISON X2O PORTAL TO GOOGLE CLOUD RUN
echo ==========================================================
echo Project: %PROJECT_ID%
echo Service: %SERVICE_NAME%
echo Region:  %REGION%
echo ==========================================================
echo.

echo 🔍 Checking Google Cloud SDK status...
call gcloud config set project %PROJECT_ID%
if %ERRORLEVEL% neq 0 (
    echo ❌ ERROR: Google Cloud SDK is not initialized or authenticated!
    echo Please run 'gcloud auth login' and try again.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo 📦 Packaging and building container in the cloud...
echo ⏳ This may take 1-2 minutes. Please wait...
call gcloud run deploy %SERVICE_NAME% --source . --port 8080 --region %REGION% --allow-unauthenticated --project %PROJECT_ID%

if %ERRORLEVEL% eq 0 (
    echo.
    echo ==========================================================
    echo 🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!
    echo 🌐 Your Jaison X2O Portal is live in the cloud!
    echo ==========================================================
) else (
    echo.
    echo ❌ ERROR: Deployment failed. Please check the logs above.
)
echo.
pause
