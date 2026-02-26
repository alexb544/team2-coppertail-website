from decimal import Decimal

SIZE_MULTIPLIERS = {
    "SMALL": Decimal("1.00"),
    "MEDIUM": Decimal("1.20"),
    "LARGE": Decimal("1.40"),
}

def estimate_total(dog, services):
    subtotal = sum((service.base_price for service in services), Decimal("0.00"))    
    mult = SIZE_MULTIPLIERS.get(getattr(dog, "size", "MEDIUM"), Decimal("1.20"))
    total = (subtotal * mult).quantize(Decimal("0.01"))
    return subtotal.quantize(Decimal("0.01")), total