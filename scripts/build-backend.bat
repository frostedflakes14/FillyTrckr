@echo off
echo Building FillyTrckr Backend...

cd /d "%~dp0\.."

REM Load configuration
for /f "tokens=1,2 delims==" %%a in (config.env) do (
    if "%%a"=="DOCKER_REGISTRY" set DOCKER_REGISTRY=%%b
    if "%%a"=="BACKEND_IMAGE" set BACKEND_IMAGE=%%b
    if "%%a"=="IMAGE_TAG" set IMAGE_TAG=%%b
)

set FULL_IMAGE=%DOCKER_REGISTRY%/%BACKEND_IMAGE%:%IMAGE_TAG%

echo Building image: %FULL_IMAGE%
docker build -t %FULL_IMAGE% -f ./backend/Dockerfile .

if %ERRORLEVEL% EQU 0 (
    echo Backend build successful!
    echo Pushing to registry...
    docker push %FULL_IMAGE%

    if %ERRORLEVEL% EQU 0 (
        echo Backend image pushed successfully!
    ) else (
        echo Failed to push backend image!
        exit /b 1
    )
) else (
    echo Backend build failed!
    exit /b 1
)
