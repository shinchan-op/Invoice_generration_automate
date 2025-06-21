from flask import Flask, request
import datetime
import requests
import json

app = Flask(__name__)

# Configuration for the inventory management system
INVENTORY_SYSTEM_URL = "http://localhost:5000/receive_transcription"

@app.route('/', methods=['GET'])
def home():
    return "Webhook server is running."

@app.route('/transcription', methods=['POST'])
def receive_transcription():
    # Log the request time
    print(f"\n===== [ Incoming Webhook at {datetime.datetime.now()} ] =====")

    # Log headers
    print(">> Headers:")
    for key, value in request.headers.items():
        print(f"{key}: {value}")

    # Try to parse JSON payload
    try:
        data = request.get_json(force=True)  # works even if Content-Type is wrong
        print(">> Parsed JSON:")
        print(data)

        # Try to extract transcript in common formats
        transcript_text = None
        if isinstance(data, dict):
            # Direct transcript field
            if 'transcript' in data:
                transcript_text = data['transcript']
                print(f">> Found transcript in 'transcript' field: {transcript_text}")
            # Nested data structure
            elif 'data' in data and isinstance(data['data'], dict):
                if 'text' in data['data']:
                    transcript_text = data['data']['text']
                    print(f">> Found transcript in 'data.text' field: {transcript_text}")
                elif 'transcription' in data['data']:
                    transcript_text = data['data']['transcription']
                    print(f">> Found transcript in 'data.transcription' field: {transcript_text}")
            # Direct text field
            elif 'text' in data:
                transcript_text = data['text']
                print(f">> Found transcript in 'text' field: {transcript_text}")

        if transcript_text:
            print(f">> Final transcript to forward: {transcript_text}")
            
            # Forward transcript to inventory management system
            forward_to_inventory_system(transcript_text)
        else:
            print(">> Transcript field not found in data.")
            print(">> Available fields:", list(data.keys()) if isinstance(data, dict) else "Not a dict")

    except Exception as e:
        print(f"!! Error parsing JSON: {e}")
        print(">> Raw body:")
        print(request.data.decode('utf-8'))

    print("===== [ End of Webhook ] =====\n")
    return '', 200

def forward_to_inventory_system(transcript_text):
    """
    Forward the transcript to the inventory management system
    """
    try:
        print(f">> Forwarding transcript to inventory system...")
        print(f">> Target URL: {INVENTORY_SYSTEM_URL}")
        
        # Prepare the data to send to inventory system
        payload = {
            'transcript': transcript_text
        }
        print(f">> Payload to send: {payload}")
        
        # Send POST request to inventory system
        response = requests.post(
            INVENTORY_SYSTEM_URL,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f">> Response status: {response.status_code}")
        print(f">> Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print(f">> Successfully forwarded transcript to inventory system")
            try:
                response_json = response.json()
                print(f">> Response JSON: {response_json}")
            except:
                print(f">> Response text: {response.text}")
        else:
            print(f">> Failed to forward transcript. Status: {response.status_code}")
            print(f">> Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f">> Error: Could not connect to inventory system at {INVENTORY_SYSTEM_URL}")
        print(f">> Make sure the inventory system is running on port 5000")
    except requests.exceptions.Timeout:
        print(f">> Error: Request to inventory system timed out")
    except Exception as e:
        print(f">> Error forwarding transcript: {e}")
        import traceback
        print(f">> Full error: {traceback.format_exc()}")

if __name__ == '__main__':
    print("Starting webhook server on port 5001...")
    print(f"Webhook server will forward transcripts to: {INVENTORY_SYSTEM_URL}")
    app.run(port=5001, debug=True) 