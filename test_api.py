#!/usr/bin/env python3
"""
Simple API test script to check if transcriptions are being received
"""
import requests
import json

def test_receive_transcription():
    """Test sending a transcription directly to the main app"""
    url = "http://localhost:5000/receive_transcription"
    payload = {
        "transcript": "Test transcription from API test script"
    }
    
    try:
        print("Sending transcription directly to main app...")
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        print(f"Response status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_transcription():
    """Test getting the latest transcription"""
    url = "http://localhost:5000/get_latest_transcription"
    
    try:
        print("\nGetting latest transcription...")
        response = requests.get(url)
        print(f"Response status: {response.status_code}")
        data = response.json()
        print(f"Latest transcription: {data.get('transcription', 'None')}")
        print(f"History count: {len(data.get('history', []))}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("🧪 API Test Script")
    print("=" * 40)
    
    # Test sending transcription
    success1 = test_receive_transcription()
    
    # Test getting transcription
    success2 = test_get_transcription()
    
    if success1 and success2:
        print("\n✅ API tests passed!")
    else:
        print("\n❌ API tests failed!")

if __name__ == "__main__":
    main() 