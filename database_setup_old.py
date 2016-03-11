import sys

from sqlalchemy import Column, ForeignKey, Integer, String
    
from sqlalchemy.ext.declarative import declarative_base
    
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

# define class for a tables
class Category(Base):
    # tell Alchemy the tablename
    __tablename__ = 'category'
    
    # create variables for columns w/appropriate attributes
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    
    # CHORE: investigate property decorator
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }

class Item(Base):
    __tablename__ = 'item'
    
    # create variables for columns w/appropriate attributes
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    
# We added this serialize function to be able to send JSON objects in a
# serializable format.  Note that the method/function resides in each class
# CHORE: figure out what the property decorator does since he didn't cover it
    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
        }


        
######## insert at end of file ############

# create an sqlite dbase object - connection differes for postgre etc
engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)