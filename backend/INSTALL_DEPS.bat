@echo off
echo ========================================
echo   Installing Required Dependencies
echo ========================================
echo.

REM Activate virtual environment
call ..\venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Virtual environment not found!
    pause
    exit /b 1
)

echo Installing Python packages...
echo.

pip install chromadb sentence-transformers httpx python-dotenv

echo.
echo ========================================
echo   Dependencies Installed!
echo ========================================
echo.
echo Now you can run:
echo   python scripts\add_to_vectorstore.py
echo.

pause
