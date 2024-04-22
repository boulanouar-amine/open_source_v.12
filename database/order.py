from sqlalchemy import create_engine, Column, Integer, Float, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'  # Name of the table in the database

    # Define columns
    id = Column(Integer, primary_key=True)
    id_customer = Column(Integer, nullable=False)
    id_produit = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    start_delivery_date = Column(Date, nullable=False)
    end_delivery_date = Column(Date, nullable=False)
    delivery_adresse = Column(String, nullable=False)
    total = Column(Float, nullable=False)