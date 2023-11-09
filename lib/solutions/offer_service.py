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

def apply_bogoo(item_count, skus_count, item_id, offers_applied):
    free_items = 0
    offer_count = 0
    item_total_price = 0
    bogoo_item_id = ITEM_TABLE.get(item_id).get("bogoo_item")
    bogoo_item_count = skus_count.get(bogoo_item_id)
            
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

def apply_group_buy(group_buy_items, item_id, offers_applied):

    group_buy_count = len(group_buy_items)
    item_count = group_buy_items.count(item_id)
    remainder_items = []
    item_total_price = 0
    if group_buy_count >= ITEM_TABLE.get(item_id).get("offer_quantity"):
        if group_buy_count % ITEM_TABLE.get(item_id).get("offer_quantity") == 0:
            quotient, _ = divmod(group_buy_count, ITEM_TABLE.get(item_id).get("offer_quantity"))
            item_total_price = (quotient * ITEM_TABLE.get(item_id).get("offer_price"))
            for item in set(group_buy_items): #prehaps change the check for group buy items to boolean
                offers_applied[item] = item_total_price
        else: #Maybe for loop here to dynamically generate the while loop (from group buy item with lowest price to highest price)
            sorted_group_buy_keys = sorted((key for key, value in ITEM_TABLE.items() if value.get("offer_type") == "GROUP_BUY"), key=lambda key: ITEM_TABLE[key]["price"])
            for key in sorted_group_buy_keys:
                while key in group_buy_items:
                    if group_buy_count % ITEM_TABLE.get(item_id).get("offer_quantity") != 0:
                        group_buy_items.remove(key)
                        remainder_items.append(key)
                        group_buy_count = len(group_buy_items)
                    else:
                        break

            #calculate group buy items

            quotient, _ = divmod(len(group_buy_items), ITEM_TABLE.get(item_id).get("offer_quantity"))
            item_total_price += quotient * ITEM_TABLE.get(item_id).get("offer_price")
            for item in set(group_buy_items): #prehaps change the check for group buy items to boolean
                offers_applied[item] = item_total_price

            #calculate remainder items TODO: test out the notiion that remainder items do bot need to be calculated here. Since they will never be more than 3 remiander items, they would be calculated individually in the else block below.
            for item in remainder_items:
                item_total_price += ITEM_TABLE.get(item).get("price")
                offers_applied[item] = offers_applied.get(item, 0) + ITEM_TABLE.get(item).get("price")

                
    else:
        item_total_price += ITEM_TABLE.get(item_id).get("price") * item_count
        offers_applied[item_id] = offers_applied.get(item_id, 0) + (ITEM_TABLE.get(item_id).get("price") * item_count)

    return item_total_price
