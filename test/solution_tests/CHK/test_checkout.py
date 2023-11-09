from lib.solutions.CHK.checkout_solution import input_validation, calculate_basket_total, apply_offer, checkout
from lib.solutions.offer_service import *

class TestCheckoutSolution():
    

    def test_input_validation(self):
        skus = "ABf"
        assert not input_validation(skus)

        skus = "AAABBB"
        assert input_validation(skus)


    def test_calculate_basket_total(self):
        skus = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
        skus_count = {item: skus.count(item) for item in skus}
        offers_applied = {}

        assert calculate_basket_total(skus_count=skus_count, offers_applied=offers_applied) == 1602

        skus = "PPPPQRUVPQRUVPQRUVSU"
        skus_count = {item: skus.count(item) for item in skus}
        offers_applied = {}


        assert calculate_basket_total(skus_count=skus_count, offers_applied=offers_applied) == 730

        skus = "BBB"
        skus_count = {item: skus.count(item) for item in skus}
        offers_applied = {}

        assert calculate_basket_total(skus_count=skus_count, offers_applied=offers_applied) == 75
    

    def test_apply_normal_pricing(self):
        item_count = 2
        item_id = "A"

        assert apply_normal_pricing(item_count=item_count, item_id=item_id) == 100

    def test_apply_price_reduct_single(self):
        #case with exact number of items(no remainders)
        item_id = "B"
        item_count = 4
        offers_applied = {}

        assert apply_price_reduct_single(item_id=item_id, item_count=item_count, offers_applied=offers_applied) == 90    

        #case with imperfect number of items (with remainders)
        item_id = "K"
        item_count = 5
        offers_applied = {}

        assert apply_price_reduct_single(item_id=item_id, item_count=item_count, offers_applied=offers_applied) == 310   

        #case with not enough items to trigger offer
        item_id = "P"
        item_count = 4
        offers_applied = {}

        assert apply_price_reduct_single(item_id=item_id, item_count=item_count, offers_applied=offers_applied) == 200

    def test_apply_price_reduct_multi(self):
        #case with exact number of items for first price reduct offer(no remainders)
        item_id = "A"
        item_count = 3
        offers_applied = {}

        assert apply_price_reduct_multi(item_id=item_id, item_count=item_count, offers_applied=offers_applied) == 130

        #case with exact number of items for second price reduct offer(no remainders)
        item_id = "H"
        item_count = 10
        offers_applied = {}

        assert apply_price_reduct_multi(item_id=item_id, item_count=item_count, offers_applied=offers_applied) == 80

        #case with enough items to trigger second price offer and enough remainders to trigger first price offer
        item_id= "V"
        item_count = 5
        offers_applied = {}

        assert apply_price_reduct_multi(item_id=item_id, item_count=item_count, offers_applied=offers_applied) == 220

        #case with enough items to trigger both price reducts offers and a remainder
        item_id= "A"
        item_count = 9
        offers_applied = {}

        assert apply_price_reduct_multi(item_id=item_id, item_count=item_count, offers_applied=offers_applied) == 380

    def test_apply_bogo(self):
        #case with exact number of items to triger bogo offer
        item_id = "F"
        item_count = 3
        offers_applied = {}

        assert apply_bogo(item_id=item_id, item_count=item_count, offers_applied=offers_applied) == 20

        #case with enough items to trigger bogo plus remainders
        item_id = "U"
        item_count = 4
        offers_applied = {}
        assert apply_bogo(item_id=item_id, item_count=item_count, offers_applied=offers_applied) == 120

    def test_apply_bogoo(self):

        #case with exact number of items to trigger bogoo (with bogoo item in basket)
        item_count = 4 #Count of items that have the offer (E's) only
        skus_count = {'E': 4, 'B': 2}
        item_id = "E"
        offers_applied = {}

        assert apply_bogoo(item_count=item_count, skus_count=skus_count, item_id=item_id, offers_applied=offers_applied) == 160

        #case with enough number of items to tigger bogoo with remainders
        item_count = 2
        skus_count = {'E': 2, 'B': 2}
        item_id = "E"
        offers_applied = {}

        assert apply_bogoo(item_count=item_count, skus_count=skus_count, item_id=item_id, offers_applied=offers_applied) == 110

    def test_apply_group_buy(self):

        #case with exact number of items to trigger group buy
        group_buy_items = ["S", "S", "T", "T", "Y", "Y"]
        item_id = "S"
        offers_applied = {}
        
        assert apply_group_buy(group_buy_items=group_buy_items, item_id=item_id, offers_applied=offers_applied) == 90

        #case with enough items to trigger group buy (with remainders)
        group_buy_items = ["S", "S", "T", "T", "Y", "X", "X", "X"]
        item_id = "S"
        offers_applied = {}
        
        assert apply_group_buy(group_buy_items=group_buy_items, item_id=item_id, offers_applied=offers_applied) == 124

        group_buy_items = ["Z", "Z", "Z", "Z", "Z", "Z", "Z", "Z"]
        item_id = "Z"
        offers_applied = {}
        
        assert apply_group_buy(group_buy_items=group_buy_items, item_id=item_id, offers_applied=offers_applied) == 132

    def test_apply_offer(self):
        # Test applying BOGO offer
        offer_type = "BOGO"
        item_id = "F"
        item_count = 3
        offers_applied={}

        assert apply_offer(offer_type=offer_type, item_id=item_id, item_count=item_count, offers_applied=offers_applied) == 20

        #Test applying BOGOO offer
        offer_type = "BOGOO"
        item_id = "E"
        item_count = 4
        offers_applied={}
        skus_count = {'E': 4, 'B': 2}

        assert apply_offer(offer_type=offer_type, item_id=item_id, item_count=item_count, offers_applied=offers_applied, skus_count=skus_count) == 160

        #Test applying PRICE REDUCT MULTI
        offer_type= "PRICE_REDUCT_MULTI"
        item_count = 5
        item_id= "A"
        offers_applied = {}
        
        assert apply_offer(offer_type=offer_type, item_id=item_id, item_count=item_count, offers_applied=offers_applied) == 200

        #Test applying PRICE REDUCT SINGLE
        offer_type= "PRICE_REDUCT_SINGLE"
        item_count = 2
        item_id= "B"
        offers_applied = {}

        assert apply_offer(offer_type=offer_type, item_id=item_id, item_count=item_count, offers_applied=offers_applied) == 45

        #Test applying GROUP BUY
        offer_type= "GROUP_BUY"
        skus_count = {'S': 2, 'T': 2, 'Y': 1, 'X': 1}
        item_id = "S"
        item_count =2
        offers_applied = {}

        assert apply_offer(offer_type=offer_type, item_id=item_id, item_count=item_count, offers_applied=offers_applied, skus_count=skus_count) == 90

        #Test no offer case
        offer_type= ""
        item_id= "D"
        item_count = 50

        assert apply_offer(offer_type=offer_type, item_id=item_id, item_count=item_count, offers_applied=offers_applied) == 750

    def test_checkout(self):

        assert checkout("ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ") == 1602

        

        
        
        
        
        


        

        


        
    

        





