from solutions.constants import ITEM_TABLE_OLD
#from offer_service import * 

# noinspection PyUnusedLocal
# skus = unicode string

ITEM_TABLE = {
    "A": {
        "price": 50,
        "offer_type": "PRICE_REDUCT_MULTI",
        "offer_price": 130,
        "offer_quantity": 3,
        "offer_type_1": "PRICE_REDUCT_MULTI",
        "offer_price_1": 200,
        "offer_quantity_1": 5,
    },
    "B": {
        "price": 30,
        "offer_type": "PRICE_REDUCT_SINGLE",
        "offer_price": 45,
        "offer_quantity": 2,
    },
    "C": {
        "price": 20,
        "offer_type": "",
        "offer_price": 0,
        "offer_quantity": 0,
    },
    "D": {
        "price": 15,
        "offer_type": "",
        "offer_price": 0,
        "offer_quantity": 0,
    },
    "E": {
        "price": 40,
        "offer_type": "BOGOO",
        "bogoo_item": "B",
        "offer_price": 0,
        "offer_quantity": 2,
    },
    "F": {
        "price": 10,
        "offer_type": "BOGO",
        "offer_price": 0,
        "offer_quantity": 2,
    },
    "G": {
        "price": 20,
        "offer_type": "",
        "offer_price": 0,
        "offer_quantity": 0,
    },
    "H": {
        "price": 10,
        "offer_type": "PRICE_REDUCT_MULTI",
        "offer_price": 45,
        "offer_quantity": 5,
        "offer_type_1": "PRICE_REDUCT_MULTI",
        "offer_price_1": 80,
        "offer_quantity_1": 10,
    },
    "I": {
        "price": 35,
        "offer_type": "",
        "offer_price": 0,
        "offer_quantity": 0,
    },
    "J": {
        "price": 60,
        "offer_type": "",
        "offer_price": 0,
        "offer_quantity": 0,
    },
    "K": {
        "price": 80,
        "offer_type": "PRICE_REDUCT_SINGLE",
        "offer_price": 150,
        "offer_quantity": 2,
    },
    "L": {
        "price": 90,
        "offer_type": "",
        "offer_price": 0,
        "offer_quantity": 0,
    },
    "M": {
        "price": 15,
        "offer_type": "",
        "offer_price": 0,
        "offer_quantity": 0,
    },
    "N": {
        "price": 40,
        "offer_type": "BOGOO",
        "bogoo_item": "M",
        "offer_price": 0,
        "offer_quantity": 3,
    },
    "O": {
        "price": 10,
        "offer_type": "",
        "offer_price": 0,
        "offer_quantity": 0,
    },
    "P": {
        "price": 50,
        "offer_type": "PRICE_REDUCT_SINGLE",
        "offer_price": 200,
        "offer_quantity": 5,
    },
    "Q": {
        "price": 30,
        "offer_type": "PRICE_REDUCT_SINGLE",
        "offer_price": 80,
        "offer_quantity": 3,
    },
    "R": {
        "price": 50,
        "offer_type": "BOGOO",
        "bogoo_item": "Q",
        "offer_price": 0,
        "offer_quantity": 3,
    },
    "S": {
        "price": 30,
        "offer_type": "",
        "offer_price": 0,
        "offer_quantity": 0,
    },
    "T": {
        "price": 20,
        "offer_type": "",
        "offer_price": 0,
        "offer_quantity": 0,
    },
    "U": {
        "price": 40,
        "offer_type": "BOGO",
        "offer_price": 0,
        "offer_quantity": 3,
    },
    "V": {
        "price": 50,
        "offer_type": "PRICE_REDUCT_MULTI",
        "offer_price": 90,
        "offer_quantity": 2,
        "offer_type_1": "PRICE_REDUCT_MULTI",
        "offer_price_1": 130,
        "offer_quantity_1": 3,
    },
    "W": {
        "price": 20,
        "offer_type": "",
        "offer_price": 0,
        "offer_quantity": 0,
    },
    "X": {
        "price": 90,
        "offer_type": "",
        "offer_price": 0,
        "offer_quantity": 0,
    },
    "Y": {
        "price": 10,
        "offer_type": "",
        "offer_price": 0,
        "offer_quantity": 0,
    },
    "Z": {
        "price": 50,
        "offer_type": "",
        "offer_price": 0,
        "offer_quantity": 0,
    },
}


def checkout(skus):
    if not input_validation(skus):
        return -1
    skus_count = {item: skus.count(item) for item in skus}
    offers_applied = {}
    return calculate_basket_total(skus_count=skus_count, offers_applied=offers_applied)

def input_validation(skus):
    
    for sku in skus:
        if sku not in ITEM_TABLE:
            return False
    return True

def calculate_basket_total(skus_count, offers_applied):
    basket_total = 0
    for sku in skus_count:
        sku_total = apply_offer(offer_type=ITEM_TABLE.get(sku).get("offer_type"), item_id=sku, item_count = skus_count.get(sku), offers_applied=offers_applied, skus_count=skus_count)
        basket_total += sku_total
    return basket_total

def apply_offer(offer_type, item_id, item_count, offers_applied, basket_total = 0, **kwargs):
                                                                                                               
    if item_id not in offers_applied:
        if offer_type == "BOGO":
            basket_total += apply_bogo(item_count=item_count, item_id=item_id, offers_applied=offers_applied)
        elif offer_type == "BOGOO":
            basket_total += apply_bogoo(item_count=item_count, kwargs=kwargs, item_id=item_id, offers_applied=offers_applied)
        elif offer_type == "PRICE_REDUCT_MULTI":
            basket_total += apply_price_reduct_multi(item_count=item_count, item_id=item_id, offers_applied=offers_applied)
        elif offer_type == "PRICE_REDUCT_SINGLE":
            basket_total += apply_price_reduct_single(item_id=item_id,item_count=item_count, offers_applied=offers_applied)
        elif not offer_type:
            basket_total += apply_normal_pricing(item_count=item_count, item_id=item_id)

    return basket_total

def apply_normal_pricing(item_count, item_id):
    item_total_price = ITEM_TABLE.get(item_id).get("price") * item_count
    return item_total_price
    
def apply_price_reduct_single(item_id, item_count, offers_applied):
    if item_count >= ITEM_TABLE.get(item_id).get("offer_quantity"):
        quotient, remainder = divmod(item_count, ITEM_TABLE.get(item_id).get("offer_quantity"))
        item_total_price = (quotient * ITEM_TABLE.get(item_id).get("offer_price")) + (remainder * ITEM_TABLE.get(item_id).get("price"))
        offers_applied[item_id] = item_total_price
    else:
        item_total_price = ITEM_TABLE.get(item_id).get("price") * item_count
    return item_total_price
    
def apply_price_reduct_multi(item_count, item_id, offers_applied):
    item_total_price = 0
    if item_count >= ITEM_TABLE.get(item_id).get("offer_quantity") and item_count < ITEM_TABLE.get(item_id).get("offer_quantity_1"):
        quotient, remainder = divmod(item_count, ITEM_TABLE.get(item_id).get("offer_quantity"))
        item_total_price = (quotient * ITEM_TABLE.get(item_id).get("offer_price")) + (remainder * ITEM_TABLE.get(item_id).get("price"))
        offers_applied[item_id] = item_total_price
    elif item_count >= ITEM_TABLE.get(item_id).get("offer_quantity_1"):
        quotient, remainder = divmod(item_count, ITEM_TABLE.get(item_id).get("offer_quantity_1"))
        if remainder >= ITEM_TABLE.get(item_id).get("offer_quantity"):
            new_q, new_r = divmod(remainder, ITEM_TABLE.get(item_id).get("offer_quantity"))
            item_total_price += (new_q * ITEM_TABLE.get(item_id).get("offer_price")) + (new_r * ITEM_TABLE.get(item_id).get("price"))
            item_total_price += (quotient * ITEM_TABLE.get(item_id).get("offer_price_1")) #Handle case where user combines 3A and 5A offers 
            offers_applied[item_id] = (new_q * ITEM_TABLE.get(item_id).get("offer_price")) + (new_r * ITEM_TABLE.get(item_id).get("price"))
            offers_applied[f"{item_id}_1"] = (quotient * ITEM_TABLE.get(item_id).get("offer_price_1"))
        else:
            item_total_price += (quotient * ITEM_TABLE.get(item_id).get("offer_price_1")) + (remainder * ITEM_TABLE.get(item_id).get("price"))
            offers_applied[f"{item_id}_1"] = item_total_price
    else:
        item_total_price = ITEM_TABLE.get(item_id).get("price") * item_count
    return item_total_price

def apply_bogo(item_count, item_id, offers_applied):
    free_items = 0
    if item_count >= ITEM_TABLE.get(item_id).get("offer_quantity") + 1:
        quotient, remainder = divmod(item_count, ITEM_TABLE.get(item_id).get("offer_quantity") + 1)
        for i in range(quotient):
            free_items += 1
        item_total_price = (item_count * ITEM_TABLE.get(item_id).get("price")) - (free_items * ITEM_TABLE.get(item_id).get("price"))
        offers_applied[item_id] = item_total_price
    else:
        item_total_price = (item_count * ITEM_TABLE.get(item_id).get("price"))
    return item_total_price

def apply_bogoo(item_count, kwargs, item_id, offers_applied):
    free_items = 0
    offer_count = 0
    item_total_price = 0
    bogoo_item_id = ITEM_TABLE.get(item_id).get("bogoo_item")
    bogoo_item_count = kwargs.get("skus_count").get(bogoo_item_id)
            
    if item_count >= ITEM_TABLE.get(item_id).get("offer_quantity") and bogoo_item_count:
        #Reset bogoo item price
        if bogoo_item_id in offers_applied:
            item_total_price -= offers_applied.get(bogoo_item_id)
   
        # calculate free bogoo items
        eligible_free_items, _ = divmod(item_count, ITEM_TABLE.get(item_id).get("offer_quantity"))
        for i in range(bogoo_item_count):
            if eligible_free_items:
                item_total_price += ITEM_TABLE.get(bogoo_item_id).get("price")
                free_items += 1
                eligible_free_items -= 1 
        item_total_price += (item_count * ITEM_TABLE.get(item_id).get("price")) - ((free_items) * ITEM_TABLE.get(bogoo_item_id).get("price"))
        offers_applied[item_id] = item_total_price
        offers_applied[bogoo_item_id] = item_total_price

        #Recalculate bogoo item's original offer if there are remaining bogoo items that qualify
        if free_items < bogoo_item_count:
            remaining_bogoo_items = (bogoo_item_count - free_items)
            if remaining_bogoo_items >= ITEM_TABLE.get(bogoo_item_id).get("offer_quantity"):
                quotient_bogoo, remainder_bogoo = divmod(remaining_bogoo_items, ITEM_TABLE.get(bogoo_item_id).get("offer_quantity"))
                item_total_price += (quotient_bogoo * ITEM_TABLE.get(bogoo_item_id).get("offer_price")) + (remainder_bogoo * ITEM_TABLE.get(bogoo_item_id).get("price"))
                offers_applied[bogoo_item_id] = item_total_price
            else:
                item_total_price += (remaining_bogoo_items * ITEM_TABLE.get(bogoo_item_id).get("price"))
    else:
        item_total_price = ITEM_TABLE.get(item_id).get("price") * item_count
    return item_total_price
