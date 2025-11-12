# Real-time Sensor Dashboard

A Dash-based dashboard that displays real-time sensor data and stress predictions from multiple ML models.

## Features

- **Real-time sensor visualization**: X, Y, Z accelerometer, EDA, Heart Rate, Temperature
- **Multi-model predictions**: Displays stress labels predicted by all models in the `models/` folder
- **Live updates**: Dashboard refreshes automatically every second
- **Color-coded predictions**: Different colors for different stress levels

## Installation

```bash
pip install -r requirements_dashboard.txt
```

## Usage

### Step 1: Start the Simulator

In one terminal, run the sensor simulator:

```bash
python sensor_simulator.py
```

You can adjust the update interval:
```bash
python sensor_simulator.py --interval 0.5  # Update every 0.5 seconds
```

### Step 2: Start the Dashboard

In another terminal, run the dashboard:

```bash
python dashboard.py
```

The dashboard will open at: **http://127.0.0.1:8050**

## Dashboard Components

1. **Status Indicator**: Shows connection status and last update time
2. **Model Predictions**: Cards showing predicted stress label and confidence for each model
3. **Accelerometer Graph**: Real-time X, Y, Z values
4. **EDA Graph**: Electrodermal activity over time
5. **Heart Rate Graph**: Heart rate in BPM
6. **Temperature Graph**: Temperature readings

## Stress Labels

- **Label 0.0**: Low stress (Blue)
- **Label 1.0**: Medium stress (Orange)
- **Label 2.0**: High stress (Red)

## Files

- `dashboard.py`: Main dashboard application
- `sensor_simulator.py`: Simulates sensor data generation
- `sensor_data.json`: Shared data file (created automatically)

## Customization

- Change update interval: Modify `UPDATE_INTERVAL` in `dashboard.py`
- Adjust number of data points displayed: Change `df.tail(100)` in `dashboard.py`
- Modify sensor ranges: Edit `generate_sensor_data()` in `sensor_simulator.py`

