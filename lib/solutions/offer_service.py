from solutions.constants import ITEM_TABLE

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
