#!/bin/bash
echo "Starting Sensor Dashboard System..."
echo ""
echo "Step 1: Starting Sensor Simulator (in background)..."
python sensor_simulator.py --interval 1.0 &
SIMULATOR_PID=$!
sleep 2
echo ""
echo "Step 2: Starting Dashboard..."
echo "Dashboard will open at http://127.0.0.1:8050"
echo ""
python dashboard.py

# Cleanup on exit
trap "kill $SIMULATOR_PID 2>/dev/null" EXIT

