def get_stock(product, specs):
    """Returns current stock for given product-spec combination"""
    stock_db = {
        # Removed TMT rods & steel coils per request
        ("steel beams", "I-section"): 25,
        ("steel plates", "10mm"): 100,
        ("steel pipes", "2-inch"): 50,
        ("steel angles", "50x50mm"): 75,
        ("steel channels", "100mm"): 40,
        ("steel wires", "3mm"): 200,
        ("steel mesh", "4x4mm"): 30,
        ("stainless steel sheets", "304-grade"): 60
    }
    return stock_db.get((product, specs), 0)

def get_price(product, specs):
    """Returns price per unit for given product-spec combination"""
    price_db = {
        ("steel beams", "I-section"): 800,
        ("steel plates", "10mm"): 600,
        ("steel pipes", "2-inch"): 1200,
        ("steel angles", "50x50mm"): 400,
        ("steel channels", "100mm"): 700,
        ("steel wires", "3mm"): 50,
        ("steel mesh", "4x4mm"): 300,
        ("stainless steel sheets", "304-grade"): 2000
    }
    return price_db.get((product, specs), 0)

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
        "stainless steel sheets": 7
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
        "stainless steel sheets": 40
    }
    return demand_db.get(product, 0)
