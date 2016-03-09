from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Base, Category, Item
 
engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



#Menu for UrbanBurger
category1 = Category(name = "Snowboards")

session.add(category1)
session.commit()

item1 = Item(name = "Lamar 160", description = "A rocking board", price = "$159.99",  category = category1)

session.add(item1)
session.commit()

item2 = Item(name = "Morrow MadMan", description = "It's Insane!", price = "$555.50", category = category1)

session.add(item2)
session.commit()

item3 = Item(name = "Rossignol Angus Pro", description = "This is the one to get", price = "$333.99", category = category1)

session.add(item3)
session.commit()



#Menu for Super Stir Fry
category2 = Category(name = "Skis")

session.add(category2)
session.commit()


item1 = Item(name = "Head Genius 180", description = "Where did these come from", price = "$259.99",  category = category2)

session.add(item1)
session.commit()

item2 = Item(name = "Salomon Fat Boys", description = "Never be scared of powder!", price = "$855.50", category = category2)

session.add(item2)
session.commit()

item3 = Item(name = "Rossignol Crazy Skis", description = "Damn those Austrians", price = "$533.99", category = category2)

session.add(item3)
session.commit()

print "added catalog items!"