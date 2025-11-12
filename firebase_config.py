"""
Firebase Configuration and Helper Functions
"""
import firebase_admin
from firebase_admin import credentials, db, firestore
import os
from datetime import datetime

# Initialize Firebase (will be done in main app)
firebase_app = None
firestore_db = None

def initialize_firebase(credential_path=None, database_url=None, use_firestore=True):
    """
    Initialize Firebase Admin SDK
    
    Parameters:
    - credential_path: Path to Firebase service account JSON file
    - database_url: Firebase Realtime Database URL (for Realtime DB)
    - use_firestore: If True, use Firestore; if False, use Realtime Database
    """
    global firebase_app, firestore_db
    
    if firebase_app is not None:
        return firebase_app
    
    try:
        if credential_path and os.path.exists(credential_path):
            cred = credentials.Certificate(credential_path)
        else:
            # Try to use default credentials (for Google Cloud environments)
            cred = credentials.ApplicationDefault()
        
        if use_firestore:
            firebase_app = firebase_admin.initialize_app(cred)
            firestore_db = firestore.client()
            print("Firebase Firestore initialized successfully")
        else:
            firebase_app = firebase_admin.initialize_app(cred, {
                'databaseURL': database_url
            })
            print("Firebase Realtime Database initialized successfully")
        
        return firebase_app
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        print("Make sure you have firebase_admin installed: pip install firebase-admin")
        return None

def save_stress_event(stress_level, confidence, sensor_data=None, model_name=None):
    """
    Save a stress event to Firebase
    
    Parameters:
    - stress_level: Predicted stress level (0, 1, or 2)
    - confidence: Confidence score (0-1)
    - sensor_data: Optional sensor readings dict
    - model_name: Optional model that made the prediction
    """
    global firestore_db
    
    if firestore_db is None:
        print("Firebase not initialized. Cannot save stress event.")
        return False
    
    try:
        event_data = {
            'timestamp': firestore.SERVER_TIMESTAMP,
            'timestamp_readable': datetime.now().isoformat(),
            'stress_level': float(stress_level),
            'confidence': float(confidence),
            'model_name': model_name,
        }
        
        if sensor_data:
            event_data['sensor_data'] = sensor_data
        
        # Save to Firestore
        doc_ref = firestore_db.collection('stress_events').add(event_data)
        print(f"Stress event saved: Level {stress_level} at {event_data['timestamp_readable']}")
        return True
        
    except Exception as e:
        print(f"Error saving stress event: {e}")
        return False

def get_stress_events(limit=100):
    """
    Retrieve recent stress events from Firebase
    
    Parameters:
    - limit: Maximum number of events to retrieve
    
    Returns:
    - List of stress event documents
    """
    global firestore_db
    
    if firestore_db is None:
        return []
    
    try:
        events_ref = firestore_db.collection('stress_events')
        events = events_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit).stream()
        
        event_list = []
        for event in events:
            event_data = event.to_dict()
            event_data['id'] = event.id
            event_list.append(event_data)
        
        return event_list
    except Exception as e:
        print(f"Error retrieving stress events: {e}")
        return []

def save_stress_event_realtime_db(stress_level, confidence, sensor_data=None, model_name=None):
    """
    Save stress event to Firebase Realtime Database (alternative to Firestore)
    """
    global firebase_app
    
    if firebase_app is None:
        print("Firebase not initialized. Cannot save stress event.")
        return False
    
    try:
        event_data = {
            'timestamp': datetime.now().isoformat(),
            'stress_level': float(stress_level),
            'confidence': float(confidence),
            'model_name': model_name,
        }
        
        if sensor_data:
            event_data['sensor_data'] = sensor_data
        
        # Save to Realtime Database
        ref = db.reference('stress_events')
        new_event_ref = ref.push(event_data)
        print(f"Stress event saved to Realtime DB: Level {stress_level}")
        return True
        
    except Exception as e:
        print(f"Error saving stress event: {e}")
        return False

