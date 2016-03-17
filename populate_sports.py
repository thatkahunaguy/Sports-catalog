from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

from database_setup import Category, Base, Item, Country, User

engine = create_engine('sqlite:///sports.db')
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


# Create dummy user
User1 = User(name="Robo BK", email="tinnyTim@udacity.com",
             picture="http://www4.pictures.zimbio.com/gi/Brian+Krzanich+Consumer+Technology+International+E-TGduxWADTl.jpg")
             
session.add(User1)
session.commit()

# Tennis category
category1 = Category(user_id=1, name="Tennis", icon="http://www.rio2016.com/sites/all/themes/rio2016_v2/img/pictos/pt/olimpicos/118/seixo/azul/tenis.png")

session.add(category1)
session.commit()

# Country flags
country1 = Country(name = "Switzerland",
             flag = "http://www.atpworldtour.com/~/media/images/flags/sui.svg", user_id=1)

session.add(country1)
session.commit()

item1 = Item(user_id=1, 
             name="Stan Wawrinka",
             sex = "Male",
             country_id = 1,
             photo = "http://www.atpworldtour.com/~/media/tennis/players/gladiator/2016/wawrinka_full_16.png",
             description= "Nicknamed 'Stan the Man' and 'Stanimal'",
             category=category1)

session.add(item1)
session.commit()

item1 = Item(user_id=1, 
             name="Belinda Bencic",
             sex = "Female",
             country_id = 1,
             photo = "http://www.wtatennis.com/namedImage/12781/player_319001.jpg",
             description= "Coached by father, Ivan and occasionally Melanie Molitor (mother of Martina Hingis); started playing at Molitor's tennis school at age 4 (started daily training with her from age 7 for eight years until 2012) ... Mother is Dana; brother is Brian",
             category=category1)

session.add(item1)
session.commit()

print "added items!"