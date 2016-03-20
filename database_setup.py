import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class Category(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)
    icon = Column(String(250))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           "icon"         : self.icon,
       }

class Country(Base):
    __tablename__ = 'country'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable = False)
    flag = Column(String(250))
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           "flag"         : self.flag,
       }
 
class Item(Base):
    __tablename__ = 'item'


    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    sex = Column(String(6))
    country_id = Column(Integer,ForeignKey('country.id'))
    country = relationship(Country)
    birthdate = Column(Date)
    photo = Column(String(250))
    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       if self.birthdate:
           bday = self.birthdate.strftime('%m-%d-%Y')
       else:
           bday = "No birthday entered"
       print "Bday: ", self.birthdate
       return {
           'name'            : self.name,
           'description'     : self.description,
           'id'              : self.id,
           'sex'             : self.sex,
           'country_id'      : self.country_id,
           'birthdate'       : bday,
           'photo'           : self.photo,
           'category_id'     : self.category_id
       }



engine = create_engine('sqlite:///sports.db')
 

Base.metadata.create_all(engine)
