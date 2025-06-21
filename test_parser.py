#!/usr/bin/env python3
"""
Test script to verify the parser can extract items from actual transcriptions
"""
from utils.parser import parse_transcript

# Test with actual transcriptions from your meeting
test_transcriptions = [
    "hundred millimeter size, one fifty rolls of steel wire,",
    "and twelve sheets of stainless steel of three zero four grade.",
    "And don't forget the ten rules of steel mesh. Yes.",
    "I need 10 pieces of 12mm steel rods, 6 meters each",
    "Can you provide 5 sheets of 2mm thick steel plates?",
    "I want to order 20 pieces of 16mm steel bars, 8 meters long",
    "Need 15 pieces of 8mm steel wire, 100 meters each",
    "Looking for 3 pieces of 25mm steel pipes, 4 meters each",
    "add 220 tmt rod",
    "add 1 100 20 tmt rods and 40 steel coils",
    "add 120 tmt rods and 40 steel coils. we also need 15 steel beams — i-section, and 60 steel plates, preferably 10mm thick. include 80 steel pipes — 2-inch size, and 30 steel angles, the standard 50x50mm ones. also, add 25 steel channels of 100mm size, 150 rolls of steel wires, and 12 sheets of stainless steel — 304-grade. and don't forget the 10 rolls of steel mesh."
]

def test_parser():
    print("🧪 Testing Parser with Actual Transcriptions")
    print("=" * 60)
    
    for i, transcript in enumerate(test_transcriptions, 1):
        print(f"\n📝 Test {i}: {transcript}")
        print("-" * 40)
        
        try:
            items = parse_transcript(transcript)
            if items:
                print(f"✅ Extracted {len(items)} items:")
                for item in items:
                    print(f"   - {item['quantity']} {item['product']} ({item['specs']})")
            else:
                print("❌ No items extracted")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()

if __name__ == "__main__":
    test_parser() 