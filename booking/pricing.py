def estimate_total(services):
    subtotal = 0
    for service in services:
        subtotal += service.base_price  

    # TODO: Adjust cost based on the dog's size (req. updating dog model)

    tax = int(subtotal * 0.07)  # set your tax rules later
    total = subtotal + tax

    return subtotal, tax, total