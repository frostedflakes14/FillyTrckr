@echo off
echo Building FillyTrckr Frontend...

cd /d "%~dp0\.."

REM Load configuration
for /f "tokens=1,2 delims==" %%a in (config.env) do (
    if "%%a"=="DOCKER_REGISTRY" set DOCKER_REGISTRY=%%b
    if "%%a"=="FRONTEND_IMAGE" set FRONTEND_IMAGE=%%b
    if "%%a"=="IMAGE_TAG" set IMAGE_TAG=%%b
)

set FULL_IMAGE=%DOCKER_REGISTRY%/%FRONTEND_IMAGE%:%IMAGE_TAG%

echo Building image: %FULL_IMAGE%
docker build -t %FULL_IMAGE% ./frontend

if %ERRORLEVEL% EQU 0 (
    echo Frontend build successful!
    echo Pushing to registry...
    docker push %FULL_IMAGE%

    if %ERRORLEVEL% EQU 0 (
        echo Frontend image pushed successfully!
    ) else (
        echo Failed to push frontend image!
        exit /b 1
    )
) else (
    echo Frontend build failed!
    exit /b 1
)
