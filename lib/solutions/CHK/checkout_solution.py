

# noinspection PyUnusedLocal
# skus = unicode string

ITEM_TABLE = {
            "A": {
                    "price": 50,
                    "offer_price": 130,
                    "offer_quantity": 3,
                    "offer_price_1": 200,
                    "offer_quantity_1": 5
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
                    },
            "E": {
                    "price": 40,
                    "offer_price": 0,
                    "offer_quantity": 2
                    },
            "F": {
                    "price": 10,
                    "offer_price": 0,
                    "offer_quantity": 2
                    }
              }

def checkout(skus):
    
    if not input_validation(skus=skus):
        return -1
    
    return calculate_basket_total(skus=skus)

def calculate_basket_total(skus):
    basket_total = 0
    a_count = skus.count("A")
    b_count = skus.count("B")
    c_count = skus.count("C")
    d_count = skus.count("D")
    e_count = skus.count("E")
    f_count = skus.count("F")

    a_total_price = 0

    offers_applied = []

    if a_count >= ITEM_TABLE.get("A").get("offer_quantity") and a_count < ITEM_TABLE.get("A").get("offer_quantity_1"):
        quotient, remainder = divmod(a_count, ITEM_TABLE.get("A").get("offer_quantity"))
        a_total_price = (quotient * ITEM_TABLE.get("A").get("offer_price")) + (remainder * ITEM_TABLE.get("A").get("price"))
        offers_applied.append("A") #Handle case of 3A for 130
    elif a_count >= ITEM_TABLE.get("A").get("offer_quantity_1"): #Handle case of 5A for 200 offer
        quotient, remainder = divmod(a_count, ITEM_TABLE.get("A").get("offer_quantity_1"))
        if remainder >= ITEM_TABLE.get("A").get("offer_quantity"):
            new_q, new_r = divmod(remainder, ITEM_TABLE.get("A").get("offer_quantity"))
            a_total_price += (new_q * ITEM_TABLE.get("A").get("offer_price")) + (new_r * ITEM_TABLE.get("A").get("price"))
            a_total_price += (quotient * ITEM_TABLE.get("A").get("offer_price_1")) #Handle case where user combines 3A and 5A offers 
            offers_applied.append("A")
            offers_applied.append("A_1")
        else:
            a_total_price += (quotient * ITEM_TABLE.get("A").get("offer_price_1")) + (remainder * ITEM_TABLE.get("A").get("price"))
            offers_applied.append("A_1")
    else:
        a_total_price = ITEM_TABLE.get("A").get("price") * a_count

    if b_count >= ITEM_TABLE.get("B").get("offer_quantity"):
        quotient, remainder = divmod(b_count, ITEM_TABLE.get("B").get("offer_quantity"))
        b_total_price = (quotient * ITEM_TABLE.get("B").get("offer_price")) + (remainder * ITEM_TABLE.get("B").get("price"))
        offers_applied.append("B")
    else:
        b_total_price = ITEM_TABLE.get("B").get("price") * b_count

    if e_count >= ITEM_TABLE.get("E").get("offer_quantity") and b_count:
        e_offer_count = 0
        if "B" in offers_applied:
            b_total_price  = ITEM_TABLE.get("B").get("price") * b_count #Reset b price to remove any B offers
        quotient, _ = divmod(e_count, ITEM_TABLE.get("E").get("offer_quantity"))
        eligible_savings = quotient * ITEM_TABLE.get("B").get("price")
        #print("eligible_savings", eligible_savings)
        for i in range(b_count): 
            if eligible_savings:
                basket_total -= ITEM_TABLE.get("B").get("price")
                eligible_savings -= ITEM_TABLE.get("B").get("price")
                e_offer_count += 1
        if e_offer_count < b_count:
            basket_total += (e_offer_count * ITEM_TABLE.get("B").get("price"))
            remaining_b = (b_count - e_offer_count)
            if remaining_b >= ITEM_TABLE.get("B").get("offer_quantity"):
                quotient_b, remainder_b = divmod(remaining_b, ITEM_TABLE.get("B").get("offer_quantity"))
                b_total_price = (quotient_b * ITEM_TABLE.get("B").get("offer_price")) + (remainder_b * ITEM_TABLE.get("B").get("price"))
                #print("b_here", b_total_price)
            else:
                b_total_price = (remaining_b * ITEM_TABLE.get("B").get("price"))
    if f_count >= ITEM_TABLE.get("F").get("offer_quantity") + 1:
        free_f = 0
        quotient, remainder = divmod(f_count, ITEM_TABLE.get("F").get("offer_quantity") + 1)
        for i in range(quotient):
            free_f += 1
        f_total_price = (f_count * ITEM_TABLE.get("F").get("price")) - (free_f * ITEM_TABLE.get("F").get("price"))
    else:
        f_total_price = (f_count * ITEM_TABLE.get("F").get("price"))        
                
        
    c_total_price = ITEM_TABLE.get("C").get("price") * c_count
    d_total_price = ITEM_TABLE.get("D").get("price") * d_count
    e_total_price = ITEM_TABLE.get("E").get("price") * e_count

    basket_total += (a_total_price + b_total_price + d_total_price + c_total_price + e_total_price + f_total_price)

    return basket_total







    """
    if a_count >= ITEM_TABLE.get("A").get("offer_quantity"):
        quotient, remainder = divmod(a_count, ITEM_TABLE.get("A").get("offer_quantity"))
        a_total_price = (quotient * ITEM_TABLE.get("A").get("offer_price")) + (remainder * ITEM_TABLE.get("A").get("price"))
        offers_applied.append("A")
    else:
        a_total_price = ITEM_TABLE.get("A").get("price") * a_count

    if b_count >= ITEM_TABLE.get("B").get("offer_quantity"):
        quotient, remainder = divmod(b_count, ITEM_TABLE.get("B").get("offer_quantity"))
        b_total_price = (quotient * ITEM_TABLE.get("B").get("offer_price")) + (remainder * ITEM_TABLE.get("B").get("price"))
    else:
        b_total_price = ITEM_TABLE.get("B").get("price") * b_count

    c_total_price = ITEM_TABLE.get("C").get("price") * c_count

    d_total_price = ITEM_TABLE.get("D").get("price") * d_count

    e_total_price = ITEM_TABLE.get("E").get("price") * e_count

    return a_total_price + b_total_price + c_total_price + d_total_price + e_total_price
    """

def input_validation(skus):
    
    for sku in skus:
        if sku not in ITEM_TABLE:
            return False
    return True
