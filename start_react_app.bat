@echo off
echo Starting Recruit Pro Application...
echo.

echo Starting FastAPI Backend...
start "FastAPI Backend" cmd /k "python api.py"

echo Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo Starting React Frontend...
cd recruit-pro-frontend
start "React Frontend" cmd /k "npm start"

echo.
echo Application starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause > nul 