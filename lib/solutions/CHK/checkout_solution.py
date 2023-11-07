from constants import ITEM_TABLE
from offer_service import * 

# noinspection PyUnusedLocal
# skus = unicode string

ITEM_TABLE_OLD = {"A": {
                    "price": 50,
                    "offer_type": "PRICE_REDUCT_MULTI",
                    "offer_price": 130,
                    "offer_quantity": 3,
                    "offer_type_1": "PRICE_REDUCT_MULTI",
                    "offer_price_1": 200,
                    "offer_quantity_1": 5
                    },
              "B": {
                    "price": 30,
                    "offer_type": "PRICE_REDUCT_SINGLE",
                    "offer_price": 45,
                    "offer_quantity": 2
                    },
              "C": {
                    "price": 20,
                    "offer_type": "",
                    "offer_price": 0,
                    "offer_quantity": 0
                    },
              "D": {
                    "price": 15,
                    "offer_type": "",
                    "offer_price": 0,
                    "offer_quantity": 0
                    },
            "E": {
                    "price": 40,
                    "offer_type": "BOGOO",
                    "bogoo_item": "B",
                    "offer_price": 0,
                    "offer_quantity": 2
                    },
            "F": {
                    "price": 10,
                    "offer_type": "BOGO",
                    "offer_price": 0,
                    "offer_quantity": 2,
                    }
                
            }



test_cases = [
    "",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "a",
    "-",
    "ABCa",
    "AxA",
    "ABCDEF",
    "A",
    "AA",
    "AAA",
    "AAAA",
    "AAAAA",
    "AAAAAA",
    "AAAAAAA",
    "AAAAAAAA",
    "AAAAAAAAA",
    "AAAAAAAAAA",
    "EE",
    "EEB",
    "EEEB",
    "EEEEBB",
    "BEBEEE",
    "A",
    "AA",
    "AAA",
    "AAAA",
    "AAAAA",
    "AAAAAA",
    "B",
    "BB",
    "BBB",
    "BBBB",
    "FF",
    "FFF",
    "FFFF",
    "FFFFFF",
    "FFFFFF",
    "ABCDEFABCDEF",
    "CDFFAECBDEAB",
    "FFABCDECBAABCABBAAAEEAAFF",
]



def checkout(skus):
    if not input_validation(skus):
        return -1
    skus_count = {item: skus.count(item) for item in skus}
    #print(skus_count)
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


for test in test_cases:
    print(test,">>>",checkout(test))

#print(checkout("KK"))
