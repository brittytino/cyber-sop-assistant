@echo off
REM Populate Vectorstore Only - Windows
REM Use this if you just need to update the vectorstore data

echo ================================================================================
echo   FAST VECTORSTORE POPULATION
echo ================================================================================
echo.

REM Activate venv
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found. Run QUICK_START.bat first.
    pause
    exit /b 1
)

cd backend

echo Running fast population script...
echo.
python scripts\fast_populate_vectorstore.py

echo.
pause
