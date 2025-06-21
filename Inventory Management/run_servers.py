import subprocess
import sys
import time
import threading
import os

def run_inventory_system():
    """Run the inventory management system"""
    print("Starting Inventory Management System on port 5000...")
    subprocess.run([sys.executable, "app.py"])

def run_webhook_server():
    """Run the webhook server"""
    print("Starting Webhook Server on port 5001...")
    subprocess.run([sys.executable, "webhook_server.py"])

def main():
    print("=== Steel Merchant Inventory System with Webhook Integration ===")
    print("This will start both servers:")
    print("1. Inventory Management System (Port 5000)")
    print("2. Webhook Server for Zoom Transcripts (Port 5001)")
    print("\nPress Ctrl+C to stop both servers")
    print("=" * 60)
    
    # Start both servers in separate threads
    inventory_thread = threading.Thread(target=run_inventory_system, daemon=True)
    webhook_thread = threading.Thread(target=run_webhook_server, daemon=True)
    
    try:
        inventory_thread.start()
        time.sleep(2)  # Give inventory system time to start
        webhook_thread.start()
        
        print("\n✅ Both servers are running!")
        print("📱 Inventory System: http://localhost:5000")
        print("🔗 Webhook Server: http://localhost:5001")
        print("📝 Webhook Endpoint: http://localhost:5001/transcription")
        print("\n💡 Configure your Zoom/Meetstream to send webhooks to:")
        print("   http://localhost:5001/transcription")
        print("\n⏳ Waiting for webhook requests...")
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping servers...")
        print("✅ Servers stopped successfully!")

if __name__ == "__main__":
    main() 