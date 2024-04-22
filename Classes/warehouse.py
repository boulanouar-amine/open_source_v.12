from product_stock import Product_stock
from typing import List

class Warehouse:
    
    def __init__(self,id:int,product_stock_list:List[Product_stock]) -> None:
        self.id = id
        self.product_stock_list = product_stock_list
        