"""
Test script for Render-deployed API
Update the URL below to match your Render service URL
"""
import requests

# UPDATE THIS URL to your Render service URL
# Format: https://your-app-name.onrender.com
RENDER_URL = "https://your-app-name.onrender.com"

def test_api():
    """Test the deployed API"""
    
    # Test home endpoint
    print("Testing home endpoint...")
    try:
        response = requests.get(f"{RENDER_URL}/")
        print(f"✅ Home: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Home failed: {e}")
    
    print()
    
    # Test health endpoint
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{RENDER_URL}/health")
        print(f"✅ Health: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health failed: {e}")
    
    print()
    
    # Test predict endpoint
    print("Testing predict endpoint...")
    try:
        response = requests.post(f"{RENDER_URL}/predict", json={
            "X": -21.0,
            "Y": -53.0,
            "Z": 27.0,
            "EDA": 0.213944,
            "HR": 75.07,
            "TEMP": 30.37
        })
        print(f"✅ Predict: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Predict failed: {e}")
        print(f"   Error details: {str(e)}")

if __name__ == "__main__":
    print("=" * 50)
    print("Render API Test")
    print("=" * 50)
    print(f"Testing: {RENDER_URL}")
    print()
    
    # Note about cold starts
    print("⚠️  Note: First request may take 30-60 seconds")
    print("   (cold start on free tier)")
    print()
    
    test_api()
    
    print()
    print("=" * 50)
    print("Test Complete!")
    print("=" * 50)

