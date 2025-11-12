"""
View stress events stored in Firebase
"""
import os
from firebase_config import initialize_firebase, get_stress_events
from datetime import datetime

def main():
    # Initialize Firebase
    cred_path = os.getenv('FIREBASE_CREDENTIAL', 'firebase_credentials.json')
    
    if not os.path.exists(cred_path):
        print(f"Error: Firebase credentials file not found: {cred_path}")
        print("Please set up Firebase credentials first (see firebase_setup.md)")
        return
    
    print("Initializing Firebase...")
    initialize_firebase(credential_path=cred_path)
    
    print("\nFetching stress events...")
    events = get_stress_events(limit=50)
    
    if not events:
        print("No stress events found.")
        return
    
    print(f"\n{'='*80}")
    print(f"Found {len(events)} stress events")
    print(f"{'='*80}\n")
    
    for i, event in enumerate(events, 1):
        timestamp = event.get('timestamp_readable', event.get('timestamp', 'N/A'))
        stress_level = event.get('stress_level', 'N/A')
        confidence = event.get('confidence', 'N/A')
        model = event.get('model_name', 'N/A')
        
        level_names = {0.0: 'Low', 1.0: 'Medium', 2.0: 'High'}
        level_name = level_names.get(stress_level, 'Unknown')
        
        print(f"{i}. {timestamp}")
        print(f"   Stress Level: {level_name} ({stress_level})")
        print(f"   Confidence: {confidence:.1%}" if isinstance(confidence, (int, float)) else f"   Confidence: {confidence}")
        print(f"   Model: {model}")
        
        if 'sensor_data' in event:
            sensor = event['sensor_data']
            print(f"   Sensors: HR={sensor.get('HR', 'N/A')}, TEMP={sensor.get('TEMP', 'N/A')}, EDA={sensor.get('EDA', 'N/A')}")
        
        print()

if __name__ == "__main__":
    main()

