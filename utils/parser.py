def parse_transcript(transcript):
    """
    Parses a sales transcript to extract product orders with explicit quantities.
    Only includes products where quantity was explicitly mentioned in the transcript.
    Excludes 'TMT rod' and 'steel coil' from available products.
    Returns list of {product, specs, quantity} dictionaries.
    """
    result = []
    transcript_lower = transcript.lower()
    
    products = {
        "steel beam": {"product": "steel beams", "specs": "I-section", "default_qty": 15},
        "steel plate": {"product": "steel plates", "specs": "10mm", "default_qty": 25},
        "steel pipe": {"product": "steel pipes", "specs": "2-inch", "default_qty": 30},
        "steel angle": {"product": "steel angles", "specs": "50x50mm", "default_qty": 40},
        "steel channel": {"product": "steel channels", "specs": "100mm", "default_qty": 20},
        "steel wire": {"product": "steel wires", "specs": "3mm", "default_qty": 100},
        "steel mesh": {"product": "steel mesh", "specs": "4x4mm", "default_qty": 10},
        "stainless steel": {"product": "stainless steel sheets", "specs": "304-grade", "default_qty": 15}
    }
    
    import re
    
    for key, details in products.items():
        singular = key
        plural = key + "s"
        pattern = r'(\d+)\s*(?:' + re.escape(singular) + '|' + re.escape(plural) + ')'
        qty_match = re.search(pattern, transcript_lower)
        if qty_match:
            result.append({
                "product": details["product"],
                "specs": details["specs"],
                "quantity": int(qty_match.group(1))
            })
    
    print(f"Parsed items: {result}")
    return result
