from constants import ITEM_TABLE
from offer_service import * 

# noinspection PyUnusedLocal
# skus = unicode string


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
