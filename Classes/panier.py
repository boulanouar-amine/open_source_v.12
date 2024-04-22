from typing import List
from order import Order

class Panier:
    def __init__(self,order_list:List[Order],delivery_adresse:str,total:float) -> None:
        
        self.order_list = order_list # list of orders
        
        self.delivery_adresse = delivery_adresse # same as customer.adresse   
        self.total = total  # calculated as the product list price * quantity   
        