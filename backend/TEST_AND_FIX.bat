@echo off
echo ========================================
echo   Tamil Nadu Stations - Troubleshooter
echo ========================================
echo.

REM Activate virtual environment
call ..\venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Virtual environment not found!
    pause
    exit /b 1
)

echo Step 1: Testing scraped data...
echo.
python scripts\test_vectorstore_setup.py
if errorlevel 1 (
    echo.
    echo ERROR: Tests failed!
    echo Please check the errors above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Tests Passed! Ready to proceed.
echo ========================================
echo.
echo Do you want to add stations to vector store? (Y/N)
set /p choice=

if /i "%choice%"=="Y" (
    echo.
    echo Adding to vector store...
    python scripts\add_to_vectorstore.py
)

pause
