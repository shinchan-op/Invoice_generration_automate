def get_stock(product, specs):
    """Returns current stock for given product-spec combination, with fallback to product only."""
    stock_db = {
        # Removed TMT rods & steel coils per request
        ("steel beams", "I-section"): 25,
        ("steel plates", "10mm"): 100,
        ("steel pipes", "2-inch"): 50,
        ("steel angles", "50x50mm"): 75,
        ("steel channels", "100mm"): 40,
        ("steel wires", "3mm"): 200,
        ("steel mesh", "4x4mm"): 30,
        ("stainless steel sheets", "304-grade"): 60,
        ("steel rods", "12mm"): 80,
        ("steel bars", "16mm"): 90,
        ("steel plates", "2mm"): 60,
        ("steel wires", "100mm"): 50,
        ("tmt rods", "12mm"): 150,
        ("steel coils", "standard"): 45
    }
    if (product, specs) in stock_db:
        return stock_db[(product, specs)]
    # Fallback: match by product only
    for (prod, sp), val in stock_db.items():
        if prod == product:
            return val
    return 0

def get_price(product, specs):
    """Returns price per unit for given product-spec combination, with fallback to product only."""
    price_db = {
        ("steel beams", "I-section"): 800,
        ("steel plates", "10mm"): 600,
        ("steel pipes", "2-inch"): 1200,
        ("steel angles", "50x50mm"): 400,
        ("steel channels", "100mm"): 700,
        ("steel wires", "3mm"): 50,
        ("steel mesh", "4x4mm"): 300,
        ("stainless steel sheets", "304-grade"): 2000,
        ("steel rods", "12mm"): 500,
        ("steel bars", "16mm"): 650,
        ("steel plates", "2mm"): 400,
        ("steel wires", "100mm"): 120,
        ("tmt rods", "12mm"): 450,
        ("steel coils", "standard"): 1800
    }
    if (product, specs) in price_db:
        return price_db[(product, specs)]
    # Fallback: match by product only
    for (prod, sp), val in price_db.items():
        if prod == product:
            return val
    return 0

def get_supplier_lead_time(product):
    """Returns supplier lead time in days"""
    lead_time_db = {
        "steel beams": 4,
        "steel plates": 3,
        "steel pipes": 2,
        "steel angles": 3,
        "steel channels": 4,
        "steel wires": 1,
        "steel mesh": 2,
        "stainless steel sheets": 7,
        "steel rods": 2,
        "steel bars": 3,
        "tmt rods": 2,
        "steel coils": 5
    }
    return lead_time_db.get(product, 3)  # Default 3 days

def get_shipping_days(pincode):
    """Returns shipping duration based on pincode"""
    return 1 if pincode.startswith("50") else 3

def get_recent_demand(product):
    """Returns last month's demand quantity"""
    demand_db = {
        "steel beams": 20,
        "steel plates": 80,
        "steel pipes": 30,
        "steel angles": 60,
        "steel channels": 35,
        "steel wires": 150,
        "steel mesh": 25,
        "stainless steel sheets": 40,
        "steel rods": 70,
        "steel bars": 45,
        "tmt rods": 120,
        "steel coils": 25
    }
    return demand_db.get(product, 0)
