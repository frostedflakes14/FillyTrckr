@echo off
echo Building all FillyTrckr containers...
echo.

call "%~dp0build-backend.bat"
if %ERRORLEVEL% NEQ 0 (
    echo Build process failed at backend!
    exit /b 1
)

echo.
call "%~dp0build-frontend.bat"
if %ERRORLEVEL% NEQ 0 (
    echo Build process failed at frontend!
    exit /b 1
)

echo.
echo ========================================
echo All containers built and pushed successfully!
echo ========================================
