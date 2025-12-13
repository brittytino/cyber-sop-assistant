@echo off
REM Check if Ollama is running
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Ollama is already running
) else (
    echo Starting Ollama...
    start /B ollama serve
    timeout /t 3 /nobreak >nul
)

REM Configure Ollama for network access
set OLLAMA_HOST=0.0.0.0:11434

echo.
echo Ollama LLM Server
echo =================
echo Running at: http://192.168.137.1:11434
echo.
echo Press any key to check models...
pause >nul

ollama list
