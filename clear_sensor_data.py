"""
Clear old sensor data to start fresh
"""
import os

DATA_FILE = "sensor_data.json"

if os.path.exists(DATA_FILE):
    # Clear the file by writing empty array
    with open(DATA_FILE, 'w') as f:
        f.write('[]')
    print(f"Cleared {DATA_FILE}")
    print("You can now restart the simulator with fresh data.")
else:
    print(f"{DATA_FILE} does not exist. Nothing to clear.")

