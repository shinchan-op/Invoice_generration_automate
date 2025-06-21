from utils.db import get_stock, get_price, get_supplier_lead_time, get_shipping_days, get_recent_demand

def enrich_cart(parsed_items, user_pincode):
    enriched = []
    for item in parsed_items:
        stock = get_stock(item['product'], item['specs'])
        price = get_price(item['product'], item['specs'])
        delivery_days = 0

        if stock >= item['quantity']:
            delivery_days = get_shipping_days(user_pincode)
        else:
            supplier_days = get_supplier_lead_time(item['product'])
            delivery_days = supplier_days + get_shipping_days(user_pincode)

        # add demand buffer
        if get_recent_demand(item['product']) > 0.8 * stock:
            delivery_days += 1

        enriched.append({
            **item,
            "stock": stock,
            "price_per_unit": price,
            "estimated_delivery_days": delivery_days,
            "subtotal": price * item['quantity']
        })
    return enriched
