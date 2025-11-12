"""
Sensor Data Simulator
Uses actual data from balanced_data.csv for realistic predictions
"""
import json
import time
import random
import pandas as pd
from datetime import datetime
import os

DATA_FILE = "sensor_data.json"
TRAINING_DATA_FILE = "balanced_data.csv"

# Load training data once at startup
_training_data = None
_current_indices = {None: 0, 0: 0, 1: 0, 2: 0}  # Track index for each stress level
_current_timestamp = None  # Track sequential timestamp

def load_training_data():
    """Load training data from CSV file"""
    global _training_data, _current_timestamp
    if _training_data is None:
        if os.path.exists(TRAINING_DATA_FILE):
            print(f"Loading training data from {TRAINING_DATA_FILE}...")
            _training_data = pd.read_csv(TRAINING_DATA_FILE)
            print(f"Loaded {len(_training_data)} data points")
            # Don't shuffle - keep original order for sequential processing
            # Initialize timestamp from first row or use current time as base
            if len(_training_data) > 0:
                try:
                    # Try to parse the first datetime from the dataset
                    first_dt_str = _training_data.iloc[0]['datetime']
                    first_dt = pd.to_datetime(first_dt_str)
                    # Convert pandas Timestamp to Python datetime
                    if hasattr(first_dt, 'to_pydatetime'):
                        _current_timestamp = first_dt.to_pydatetime()
                    else:
                        _current_timestamp = first_dt
                except:
                    # If parsing fails, use current time as base
                    _current_timestamp = datetime.now()
            else:
                _current_timestamp = datetime.now()
        else:
            raise FileNotFoundError(f"Training data file not found: {TRAINING_DATA_FILE}")
    return _training_data

def generate_sensor_data(stress_level=None, shuffle=True):
    """
    Get actual sensor data from training dataset
    
    Parameters:
    - stress_level: If None, uses data in order. If 0, 1, or 2, filters by that label
    - shuffle: If True, randomly selects from matching data
    """
    global _current_indices, _training_data, _current_timestamp
    
    # Load training data if not already loaded
    if _training_data is None:
        load_training_data()
    
    # Filter by stress level if specified
    if stress_level is not None:
        filtered_data = _training_data[_training_data['label'] == float(stress_level)]
        if len(filtered_data) == 0:
            # Fallback to all data if no matches
            filtered_data = _training_data
        if shuffle:
            row = filtered_data.sample(n=1).iloc[0]
        else:
            idx = _current_indices[stress_level]
            row = filtered_data.iloc[idx % len(filtered_data)]
            _current_indices[stress_level] = (idx + 1) % len(filtered_data)
    else:
        # Use data in order (or shuffled)
        if shuffle:
            row = _training_data.sample(n=1).iloc[0]
        else:
            idx = _current_indices[None]
            row = _training_data.iloc[idx % len(_training_data)]
            _current_indices[None] = (idx + 1) % len(_training_data)
    
    # Generate sequential timestamp (increment by 1 second each time)
    if _current_timestamp is None:
        _current_timestamp = datetime.now()
    
    # Format timestamp to match original dataset format (with microseconds)
    timestamp_str = _current_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
    
    # Increment timestamp for next call (add 1 second)
    from datetime import timedelta
    _current_timestamp += timedelta(seconds=1)
    
    # Convert to dict with sequential timestamp
    data = {
        'X': float(row['X']),
        'Y': float(row['Y']),
        'Z': float(row['Z']),
        'EDA': float(row['EDA']),
        'HR': float(row['HR']),
        'TEMP': float(row['TEMP']),
        'timestamp': timestamp_str
    }
    
    return data

def save_sensor_data(data):
    """Save sensor data to JSON file"""
    # Read existing data
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                all_data = json.load(f)
        except:
            all_data = []
    else:
        all_data = []
    
    # Append new data
    all_data.append(data)
    
    # Keep only last 1000 readings
    if len(all_data) > 1000:
        all_data = all_data[-1000:]
    
    # Save back
    with open(DATA_FILE, 'w') as f:
        json.dump(all_data, f, indent=2)

def run_simulator(interval=1.0, stress_level=None, cycle_stress=False, sequential=False):
    """
    Run the sensor simulator using actual training data
    
    Parameters:
    - interval: Update interval in seconds
    - stress_level: Fixed stress level (0, 1, 2) or None for all data
    - cycle_stress: If True, cycles through stress levels 0->1->2->0...
    - sequential: If True, goes through data sequentially; if False, randomly samples
    """
    # Load training data
    try:
        load_training_data()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    
    print("Starting sensor simulator (using ACTUAL training data)...")
    print(f"Data source: {TRAINING_DATA_FILE}")
    print(f"Data will be saved to: {DATA_FILE}")
    print(f"Update interval: {interval} seconds")
    if stress_level is not None:
        print(f"Filtering by stress level: {stress_level}")
    elif cycle_stress:
        print("Cycling through stress levels: 0 -> 1 -> 2 -> 0...")
    else:
        print("Using all data (random sampling)" if not sequential else "Using all data (sequential)")
    print("Press Ctrl+C to stop\n")
    
    current_cycle_level = 0
    cycle_count = 0
    
    try:
        while True:
            if cycle_stress:
                # Cycle through stress levels every 10 readings
                if cycle_count % 10 == 0:
                    current_cycle_level = (current_cycle_level + 1) % 3
                sensor_data = generate_sensor_data(stress_level=current_cycle_level, shuffle=not sequential)
                cycle_count += 1
            else:
                sensor_data = generate_sensor_data(stress_level=stress_level, shuffle=not sequential)
            
            save_sensor_data(sensor_data)
            
            stress_indicator = ""
            if cycle_stress:
                stress_indicator = f" [Level {current_cycle_level}]"
            
            print(f"[{sensor_data['timestamp']}] "
                  f"X:{sensor_data['X']:.1f} Y:{sensor_data['Y']:.1f} Z:{sensor_data['Z']:.1f} "
                  f"EDA:{sensor_data['EDA']:.3f} HR:{sensor_data['HR']:.1f} TEMP:{sensor_data['TEMP']:.2f}"
                  f"{stress_indicator}")
            
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\nSimulator stopped.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Sensor Data Simulator (uses actual training data)")
    parser.add_argument("--interval", type=float, default=1.0,
                       help="Update interval in seconds (default: 1.0)")
    parser.add_argument("--stress-level", type=int, choices=[0, 1, 2], default=None,
                       help="Fixed stress level: 0=Low, 1=Medium, 2=High (default: all data)")
    parser.add_argument("--cycle", action="store_true",
                       help="Cycle through stress levels 0->1->2->0...")
    parser.add_argument("--sequential", action="store_true",
                       help="Go through data sequentially instead of random sampling")
    
    args = parser.parse_args()
    run_simulator(
        interval=args.interval, 
        stress_level=args.stress_level, 
        cycle_stress=args.cycle,
        sequential=args.sequential
    )

