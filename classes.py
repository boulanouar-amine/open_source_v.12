class Customer:
    def __init__(self, id, nom, prenom, adresse, telephone):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.adresse = adresse
        self.telephone = telephone

class Product:
    def __init__(self, id, nom, description, prix):
        self.id = id
        self.nom = nom
        self.description = description
        self.prix = prix

class OrderContains:
    def __init__(self, id_order, id_produit, quantite, preferred_time_slot, delivery_adresse, total):
        self.id_order = id_order
        self.id_produit = id_produit
        self.quantite = quantite
        self.preferred_time_slot = preferred_time_slot
        self.delivery_adresse = delivery_adresse
        self.total = total        