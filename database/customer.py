from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers' 
    
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    adresse = Column(String)
    telephone = Column(String)