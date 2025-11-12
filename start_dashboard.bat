@echo off
echo Starting Sensor Dashboard System...
echo.
echo Step 1: Starting Sensor Simulator (in background)...
start "Sensor Simulator" cmd /k "python sensor_simulator.py --interval 1.0"
timeout /t 2 /nobreak >nul
echo.
echo Step 2: Starting Dashboard...
echo Dashboard will open at http://127.0.0.1:8050
echo.
python dashboard.py

