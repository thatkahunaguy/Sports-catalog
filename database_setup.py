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
    # NOTE: I didn't cascade delete from User as unclear if I'd want to get
    #       rid of items & categories if I delete a user.  Seems more likely
    #       I'd want to implement functionality to transfer ownership of
    #       all the users categories & items as some type of admin function
    #       as currently set up if I delete a user there will be orphans in
    #       the database...but since I don't have user delete functionality...
    categories = relationship("Category", back_populates='user')
    items = relationship("Item", back_populates='user')

class Category(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User, back_populates='categories')
    icon = Column(String(250))
    items = relationship("Item", back_populates='category', cascade="save-update, merge, delete")
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
    # Don't see a need to backpopulate user - is this ok?
    user = relationship("User")
    items = relationship("Item", back_populates='country')


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
    country = relationship("Country", back_populates='items')
    birthdate = Column(Date)
    photo = Column(String(250))
    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship("Category", back_populates='items')
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship("User", back_populates='items')


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       if self.birthdate:
           bday = self.birthdate.strftime('%m-%d-%Y')
       else:
           bday = "No birthday entered"
       # print "Bday: ", self.birthdate
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
