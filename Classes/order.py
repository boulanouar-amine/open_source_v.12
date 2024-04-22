from datetime import date

class Order:
    
    def __init__(self,id_customer:int,id_produit:int, quantity:int, start_delivery_date:date,end_delivery_date:date, delivery_adresse:str, total:float):
        self.id_customer = id_customer
        self.id_produit = id_produit
        self.quantity = quantity
        self.start_delivery_date = start_delivery_date # the start date of the preferred delivery date
        self.end_delivery_date = end_delivery_date  # the end date of the preferred delivery date
        self.delivery_adresse = delivery_adresse # same as customer.adresse
        self.total = total  # calculated as the product price * quantity   