def parse_transcript(transcript):
    """
    Parses a sales transcript to extract product orders with explicit quantities.
    Handles various natural language formats for steel product orders.
    Returns list of {product, specs, quantity} dictionaries.
    """
    result = []
    transcript_lower = transcript.lower()
    
    # Define products with multiple possible names and specifications
    products = {
        "steel wire": {
            "product": "steel wires",
            "specs": "3mm",
            "patterns": [
                r'(\d+)\s*(?:rolls?|pieces?|meters?|m)\s*(?:of\s*)?steel\s*wire',
                r'steel\s*wire.*?(\d+)\s*(?:rolls?|pieces?|meters?|m)',
                r'(\d+)\s*(?:rolls?|pieces?|meters?|m).*?steel\s*wire'
            ]
        },
        "steel rod": {
            "product": "steel rods",
            "specs": "12mm",
            "patterns": [
                r'(\d+)\s*(?:pieces?|meters?|m)\s*(?:of\s*)?steel\s*rods?',
                r'steel\s*rods?.*?(\d+)\s*(?:pieces?|meters?|m)',
                r'(\d+)\s*(?:pieces?|meters?|m).*?steel\s*rods?'
            ]
        },
        "tmt rod": {
            "product": "tmt rods",
            "specs": "12mm",
            "patterns": [
                r'(\d+)\s*(?:pieces?|meters?|m)\s*(?:of\s*)?tmt\s*rods?',
                r'tmt\s*rods?.*?(\d+)\s*(?:pieces?|meters?|m)',
                r'(\d+)\s*(?:pieces?|meters?|m).*?tmt\s*rods?'
            ]
        },
        "steel bar": {
            "product": "steel bars",
            "specs": "16mm",
            "patterns": [
                r'(\d+)\s*(?:pieces?|meters?|m)\s*(?:of\s*)?steel\s*bars?',
                r'steel\s*bars?.*?(\d+)\s*(?:pieces?|meters?|m)',
                r'(\d+)\s*(?:pieces?|meters?|m).*?steel\s*bars?'
            ]
        },
        "stainless steel": {
            "product": "stainless steel sheets",
            "specs": "304-grade",
            "patterns": [
                r'(\d+)\s*(?:sheets?|pieces?|meters?|m)\s*(?:of\s*)?stainless\s*steel',
                r'stainless\s*steel.*?(\d+)\s*(?:sheets?|pieces?|meters?|m)',
                r'(\d+)\s*(?:sheets?|pieces?|meters?|m).*?stainless\s*steel'
            ]
        },
        "steel plate": {
            "product": "steel plates",
            "specs": "10mm",
            "patterns": [
                r'(\d+)\s*(?:sheets?|pieces?|meters?|m)\s*(?:of\s*)?steel\s*plates?',
                r'steel\s*plates?.*?(\d+)\s*(?:sheets?|meters?|m)',
                r'(\d+)\s*(?:sheets?|pieces?|meters?|m).*?steel\s*plates?'
            ]
        },
        "steel pipe": {
            "product": "steel pipes",
            "specs": "2-inch",
            "patterns": [
                r'(\d+)\s*(?:pieces?|meters?|m)\s*(?:of\s*)?steel\s*pipes?',
                r'steel\s*pipes?.*?(\d+)\s*(?:pieces?|meters?|m)',
                r'(\d+)\s*(?:pieces?|meters?|m).*?steel\s*pipes?'
            ]
        },
        "steel beam": {
            "product": "steel beams",
            "specs": "I-section",
            "patterns": [
                r'(\d+)\s*(?:pieces?|meters?|m)\s*(?:of\s*)?steel\s*beams?',
                r'steel\s*beams?.*?(\d+)\s*(?:pieces?|meters?|m)',
                r'(\d+)\s*(?:pieces?|meters?|m).*?steel\s*beams?'
            ]
        },
        "steel mesh": {
            "product": "steel mesh",
            "specs": "4x4mm",
            "patterns": [
                r'(\d+)\s*(?:pieces?|sheets?|meters?|m)\s*(?:of\s*)?steel\s*mesh',
                r'steel\s*mesh.*?(\d+)\s*(?:pieces?|sheets?|meters?|m)',
                r'(\d+)\s*(?:pieces?|sheets?|meters?|m).*?steel\s*mesh'
            ]
        },
        "steel coil": {
            "product": "steel coils",
            "specs": "standard",
            "patterns": [
                r'(\d+)\s*(?:pieces?|rolls?|meters?|m)\s*(?:of\s*)?steel\s*coils?',
                r'steel\s*coils?.*?(\d+)\s*(?:pieces?|rolls?|meters?|m)',
                r'(\d+)\s*(?:pieces?|rolls?|meters?|m).*?steel\s*coils?'
            ]
        },
        "steel angle": {
            "product": "steel angles",
            "specs": "50x50mm",
            "patterns": [
                r'(\d+)\s*(?:pieces?|meters?|m)\s*(?:of\s*)?steel\s*angles?',
                r'steel\s*angles?.*?(\d+)\s*(?:pieces?|meters?|m)',
                r'(\d+)\s*(?:pieces?|meters?|m).*?steel\s*angles?'
            ]
        },
        "steel channel": {
            "product": "steel channels",
            "specs": "100mm",
            "patterns": [
                r'(\d+)\s*(?:pieces?|meters?|m)\s*(?:of\s*)?steel\s*channels?',
                r'steel\s*channels?.*?(\d+)\s*(?:pieces?|meters?|m)',
                r'(\d+)\s*(?:pieces?|meters?|m).*?steel\s*channels?'
            ]
        }
    }
    
    import re
    
    # Enhanced number mapping for natural language
    number_mapping = {
        # Basic numbers
        'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
        'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'ten': '10',
        'eleven': '11', 'twelve': '12', 'thirteen': '13', 'fourteen': '14', 'fifteen': '15',
        'sixteen': '16', 'seventeen': '17', 'eighteen': '18', 'nineteen': '19', 'twenty': '20',
        'thirty': '30', 'forty': '40', 'fifty': '50', 'sixty': '60', 'seventy': '70',
        'eighty': '80', 'ninety': '90', 'hundred': '100', 'thousand': '1000',
        
        # Compound numbers
        'twenty one': '21', 'twenty two': '22', 'twenty three': '23', 'twenty four': '24', 'twenty five': '25',
        'twenty six': '26', 'twenty seven': '27', 'twenty eight': '28', 'twenty nine': '29',
        'thirty one': '31', 'thirty two': '32', 'thirty three': '33', 'thirty four': '34', 'thirty five': '35',
        'thirty six': '36', 'thirty seven': '37', 'thirty eight': '38', 'thirty nine': '39',
        'forty one': '41', 'forty two': '42', 'forty three': '43', 'forty four': '44', 'forty five': '45',
        'forty six': '46', 'forty seven': '47', 'forty eight': '48', 'forty nine': '49',
        'fifty one': '51', 'fifty two': '52', 'fifty three': '53', 'fifty four': '54', 'fifty five': '55',
        'fifty six': '56', 'fifty seven': '57', 'fifty eight': '58', 'fifty nine': '59',
        'sixty one': '61', 'sixty two': '62', 'sixty three': '63', 'sixty four': '64', 'sixty five': '65',
        'sixty six': '66', 'sixty seven': '67', 'sixty eight': '68', 'sixty nine': '69',
        'seventy one': '71', 'seventy two': '72', 'seventy three': '73', 'seventy four': '74', 'seventy five': '75',
        'seventy six': '76', 'seventy seven': '77', 'seventy eight': '78', 'seventy nine': '79',
        'eighty one': '81', 'eighty two': '82', 'eighty three': '83', 'eighty four': '84', 'eighty five': '85',
        'eighty six': '86', 'eighty seven': '87', 'eighty eight': '88', 'eighty nine': '89',
        'ninety one': '91', 'ninety two': '92', 'ninety three': '93', 'ninety four': '94', 'ninety five': '95',
        'ninety six': '96', 'ninety seven': '97', 'ninety eight': '98', 'ninety nine': '99',
        
        # Hundreds
        'one hundred': '100', 'two hundred': '200', 'three hundred': '300', 'four hundred': '400', 'five hundred': '500',
        'six hundred': '600', 'seven hundred': '700', 'eight hundred': '800', 'nine hundred': '900',
        
        # Special patterns
        'one fifty': '150', 'two fifty': '250', 'three fifty': '350', 'four fifty': '450', 'five fifty': '550',
        'six fifty': '650', 'seven fifty': '750', 'eight fifty': '850', 'nine fifty': '950',
        'one twenty': '120', 'two twenty': '220', 'three twenty': '320', 'four twenty': '420', 'five twenty': '520',
        'six twenty': '620', 'seven twenty': '720', 'eight twenty': '820', 'nine twenty': '920'
    }
    
    # Replace written numbers with digits (longest first to avoid partial matches)
    sorted_numbers = sorted(number_mapping.keys(), key=len, reverse=True)
    for word in sorted_numbers:
        digit = number_mapping[word]
        transcript_lower = re.sub(r'\b' + re.escape(word) + r'\b', digit, transcript_lower)
    
    # Handle special patterns
    transcript_lower = re.sub(r'three\s+zero\s+four', '304', transcript_lower)
    transcript_lower = re.sub(r'fifty\s+x\s+fifty', '50x50', transcript_lower)
    transcript_lower = re.sub(r'four\s+x\s+four', '4x4', transcript_lower)
    
    # Handle ranges like "1 100 20" -> "120"
    transcript_lower = re.sub(r'(\d+)\s+(\d+)\s+(\d+)', lambda m: str(int(m.group(1)) + int(m.group(2)) + int(m.group(3))), transcript_lower)
    
    print(f"Processed transcript: {transcript_lower}")
    
    for product_name, details in products.items():
        for pattern in details["patterns"]:
            match = re.search(pattern, transcript_lower)
            if match:
                quantity = int(match.group(1))
                result.append({
                    "product": details["product"],
                    "specs": details["specs"],
                    "quantity": quantity
                })
                print(f"Found {product_name}: {quantity} {details['product']}")
                break  # Found this product, move to next
    
    # Handle specific patterns from your transcriptions
    # "hundred millimeter size, one fifty rolls of steel wire"
    if "hundred millimeter" in transcript_lower and "steel wire" in transcript_lower:
        wire_match = re.search(r'(\d+)\s*rolls?\s*of\s*steel\s*wire', transcript_lower)
        if wire_match:
            result.append({
                "product": "steel wires",
                "specs": "100mm",
                "quantity": int(wire_match.group(1))
            })
            print(f"Found steel wire with 100mm specs: {wire_match.group(1)} rolls")
    
    # "twelve sheets of stainless steel of three zero four grade"
    if "stainless steel" in transcript_lower and "three zero four" in transcript_lower:
        ss_match = re.search(r'(\d+)\s*sheets?\s*of\s*stainless\s*steel', transcript_lower)
        if ss_match:
            result.append({
                "product": "stainless steel sheets",
                "specs": "304-grade",
                "quantity": int(ss_match.group(1))
            })
            print(f"Found stainless steel 304-grade: {ss_match.group(1)} sheets")
    
    # Handle "ten rules of steel mesh"
    if "steel mesh" in transcript_lower:
        mesh_match = re.search(r'(\d+)\s*(?:rules?|pieces?|sheets?)\s*of\s*steel\s*mesh', transcript_lower)
        if mesh_match:
            result.append({
                "product": "steel mesh",
                "specs": "4x4mm",
                "quantity": int(mesh_match.group(1))
            })
            print(f"Found steel mesh: {mesh_match.group(1)} pieces")
    
    # Extract specifications from the text (like 12mm, 16mm, etc.)
    for item in result:
        # Look for size specifications in the text
        size_match = re.search(r'(\d+mm)', transcript_lower)
        if size_match:
            item['specs'] = size_match.group(1)
            print(f"Updated specs for {item['product']}: {item['specs']}")
    
    print(f"Parsed items: {result}")
    return result
