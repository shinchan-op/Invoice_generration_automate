#!/usr/bin/env python3
"""
Test script to simulate sending transcriptions to the webhook server
"""
import requests
import json
import time
import random

# Sample transcriptions for testing
SAMPLE_TRANSCRIPTIONS = [
    "I need 10 pieces of 12mm steel rods, 6 meters each",
    "Can you provide 5 sheets of 2mm thick steel plates?",
    "I want to order 20 pieces of 16mm steel bars, 8 meters long",
    "Need 15 pieces of 8mm steel wire, 100 meters each",
    "Looking for 3 pieces of 25mm steel pipes, 4 meters each"
]

def send_test_transcription(transcript):
    """Send a test transcription to the webhook server"""
    webhook_url = "http://localhost:5001/transcription"
    
    # Simulate different webhook payload formats
    payload_formats = [
        {"transcript": transcript},
        {"data": {"text": transcript}},
        {"data": {"transcription": transcript}},
        {"text": transcript}
    ]
    
    payload = random.choice(payload_formats)
    
    try:
        print(f"Sending transcription: {transcript}")
        print(f"Payload format: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            webhook_url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Successfully sent transcription to webhook server")
        else:
            print(f"❌ Failed to send transcription: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to webhook server")
        print("Make sure the webhook server is running on port 5001")
    except Exception as e:
        print(f"❌ Error sending transcription: {e}")
    
    print("-" * 50)

def main():
    print("🧪 Webhook Server Test Script")
    print("=" * 50)
    print("This script will send test transcriptions to your webhook server")
    print("Make sure both servers are running:")
    print("- Main app: python app.py (port 5000)")
    print("- Webhook server: python webhook_server.py (port 5001)")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Send random sample transcription")
        print("2. Send custom transcription")
        print("3. Send multiple transcriptions")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            transcript = random.choice(SAMPLE_TRANSCRIPTIONS)
            send_test_transcription(transcript)
            
        elif choice == "2":
            transcript = input("Enter your transcription: ").strip()
            if transcript:
                send_test_transcription(transcript)
            else:
                print("❌ Please enter a valid transcription")
                
        elif choice == "3":
            count = input("How many transcriptions to send? (default: 5): ").strip()
            try:
                count = int(count) if count else 5
                for i in range(count):
                    transcript = random.choice(SAMPLE_TRANSCRIPTIONS)
                    send_test_transcription(transcript)
                    time.sleep(2)  # Wait 2 seconds between requests
            except ValueError:
                print("❌ Please enter a valid number")
                
        elif choice == "4":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main() 