from typing import List
from product import Product

class Product_stock:
    def __init__(self,id:int,product:Product,quantity:int) -> None:
        self.id = id
        self.product = product
        self.quantity = quantity  
        