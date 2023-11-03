

# noinspection PyUnusedLocal
# skus = unicode string

ITEM_TABLE = {
            "A": {
                    "price": 50,
                    "offer_price": 130,
                    "offer_quantity": 3
                    },
            "B": {
                    "price": 30,
                    "offer_price": 45,
                    "offer_quantity": 2
                    },
            "C": {
                    "price": 20,
                    "offer_price": 0,
                    "offer_quantity": 0
                    },
            "D": {
                    "price": 15,
                    "offer_price": 0,
                    "offer_quantity": 0
                    }
              }

def checkout(skus):
    
    if not input_validation(skus=skus):
        return -1
    
    return calculate_basket_total(skus=skus)

def calculate_basket_total(skus):
    a_count = skus.count("A")
    b_count = skus.count("B")
    c_count = skus.count("C")
    d_count = skus.count("D")

    if a_count >= ITEM_TABLE.get("A").get("offer_quantity"):
        quotient, remainder = divmod(a_count, ITEM_TABLE.get("A").get("offer_quantity"))
        a_total_price = (quotient * ITEM_TABLE.get("A").get("offer_price")) + (remainder * ITEM_TABLE.get("A").get("offer_quantity"))
    else:
        a_total_price = ITEM_TABLE.get("A").get("price") * a_count

    if b_count >= ITEM_TABLE.get("B").get("offer_quantity"):
        quotient, remainder = divmod(b_count, ITEM_TABLE.get("B").get("offer_quantity"))
        b_total_price = (quotient * ITEM_TABLE.get("B").get("offer_price")) + (remainder * ITEM_TABLE.get("B").get("offer_quantity"))
    else:
        b_total_price = ITEM_TABLE.get("B").get("price") * b_count

    c_total_price = ITEM_TABLE.get("C").get("price") * c_count

    d_total_price = ITEM_TABLE.get("D").get("price") * d_count

    return a_total_price + b_total_price + c_total_price + d_total_price

def input_validation(skus):
    
    for sku in skus:
        if sku not in ITEM_TABLE:
            return False
        return True

