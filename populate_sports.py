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

# Soccer category
category2 = Category(user_id=1, name="Soccer", icon="http://www.rio2016.com/sites/all/themes/rio2016_v2/img/pictos/pt/olimpicos/118/seixo/azul/futebol.png")

session.add(category2)
session.commit()

# Beach Volleyball category
category3 = Category(user_id=1, name="Beach Volleyball", icon="http://www.rio2016.com/sites/all/themes/rio2016_v2/img/pictos/pt/olimpicos/118/seixo/azul/volei-de-praia.png")

session.add(category3)
session.commit()

# Country flags
country1 = Country(name = "Switzerland",
             flag = "http://www.atpworldtour.com/~/media/images/flags/sui.svg", user_id=1)

session.add(country1)
session.commit()
country2 = Country(name = "United States of America",
             flag = "http://www.atpworldtour.com/~/media/images/flags/usa.svg", user_id=1)

session.add(country2)
session.commit()
country3 = Country(name = "Great Britain",
             flag = "http://www.atpworldtour.com/~/media/images/flags/gbr.svg", user_id=1)

session.add(country3)
session.commit()
country4 = Country(name = "Spain",
             flag = "http://www.atpworldtour.com/~/media/images/flags/esp.svg", user_id=1)

session.add(country4)
session.commit()
country5 = Country(name = "Germany",
             flag = "http://www.atpworldtour.com/~/media/images/flags/ger.svg", user_id=1)

session.add(country5)
session.commit()

item1 = Item(user_id=1, 
             name="Stan Wawrinka",
             sex = "Male",
             country_id = 1,
             birthdate = date(1985, 3, 28),
             photo = "http://www.atpworldtour.com/~/media/tennis/players/gladiator/2016/wawrinka_full_16.png",
             description= "Nicknamed 'Stan the Man' and 'Stanimal'",
             category=category1)

session.add(item1)
session.commit()

item1 = Item(user_id=1, 
             name="Belinda Bencic",
             sex = "Female",
             country_id = 1,
             birthdate = date(1997, 3, 10),
             photo = "http://www.wtatennis.com/namedImage/12781/player_319001.jpg",
             description= "Coached by father, Ivan and occasionally Melanie Molitor (mother of Martina Hingis); started playing at Molitor's tennis school at age 4 (started daily training with her from age 7 for eight years until 2012) ... Mother is Dana; brother is Brian",
             category=category1)

session.add(item1)
session.commit()

item1 = Item(user_id=1, 
             name="Roger Federer",
             sex = "Male",
             country_id = 1,
             birthdate = date(1981, 8, 8),
             photo = "http://www.atpworldtour.com/~/media/tennis/players/gladiator/vibrant/federer-full15.png",
             description= "Began playing tennis at age 8.  Idols growing up were Stefan Edberg, Boris Becker and Pete Sampras.",
             category=category1)

session.add(item1)
session.commit()

item1 = Item(user_id=1, 
             name="Andy Murray",
             sex = "Male",
             country_id = 3,
             birthdate = date(1987, 5, 15),
             photo = "http://www.atpworldtour.com/~/media/tennis/players/gladiator/vibrant/murray-full15.png",
             description= "Began playing at age 3.  Mother, Judy, is current British Fed Cup captain and father, William, is a retail Area Manager. Has 1 older brother Jamie (born Feb. 13, 1986), who also plays on the ATP circuit.  Grew up playing football and tennis and was once offered trials with Glasgow Rangers FC",
             category=category1)

session.add(item1)
session.commit()

item1 = Item(user_id=1, 
             name="Rafael Nadal",
             sex = "Male",
             country_id = 4,
             birthdate = date(1986, 6, 3),
             photo = "http://www.atpworldtour.com/~/media/tennis/players/gladiator/2016/nadal_full_16.png",
             description= "Began playing tennis at age 4 with his uncle Toni.  Plays left-handed but writes right-handed. Used to play with 2-handed forehand and backhand before his uncle made him change at age 9 or 10 to a 1-handed forehand",
             category=category1)

session.add(item1)
session.commit()

item1 = Item(user_id=1, 
             name="Angelique Kerber",
             sex = "Female",
             country_id = 5,
             birthdate = date(1988, 1, 18),
             photo = "http://www.wtatennis.com/namedImage/12781/player_311470.jpg",
             description= "Coached by Torben Beltz ... Mother's name is Beata (also her manager); father's name is Slawek; has one sister, Jessica ... Started playing tennis at age 3 ... Likes all surfaces ... Speaks German, Polish and English",
             category=category1)

session.add(item1)
session.commit()

item1 = Item(user_id=1, 
             name="Coco Vandeweghe",
             sex = "Female",
             country_id = 2,
             birthdate = date(1991, 12, 6),
             photo = "http://www.wtatennis.com/namedImage/12781/player_314464.jpg",
             description= "Coached by Craig Kardon ... Mother's name is Tauna (represented USA at Olympics for swimming in 1976 and volleyball in 1984); grandfather's name is Ernie (played for New York Knicks in 1950s)",
             category=category1)

session.add(item1)
session.commit()

item1 = Item(user_id=1, 
             name="Andreas Iniesta",
             sex = "Male",
             country_id = 4,
             birthdate = date(1984, 5, 11),
             photo = "http://media4.fcbarcelona.com/media/asset_publics/resources/000/179/582/size_1000x562/1000x562_INIESTA.v1439396180.jpg",
             description= "Andreas Iniesta joined Barca as a twelve-year-old in 1996 after scouts had spotted him at the Brunette Tournament playing for Albacete..",
             category=category2)

session.add(item1)
session.commit()

item1 = Item(user_id=1, 
             name="John Terry",
             sex = "Male",
             country_id = 3,
             birthdate = date(1980, 12, 7),
             photo = "http://a.espncdn.com/combiner/i/?img=/soccernet/i/players/130x180/8931.jpg&w=130&h=180&scale=crop&site=espnfc",
             description= "John George Terry is an English professional footballer who plays for and captains Chelsea. He commonly plays as a centre back.",
             category=category2)

session.add(item1)
session.commit()

item1 = Item(user_id=1, 
             name="Thomas Muller",
             sex = "Male",
             country_id = 5,
             birthdate = date(1989, 9, 13),
             photo = "http://a.espncdn.com/combiner/i/?img=/soccernet/i/players/130x180/123465.jpg&w=130&h=180&scale=crop&site=espnfc",
             description= "Thomas Muller is a German professional footballer who plays for Bayern Munich and the Germany national team. Mller plays as a midfielder or forward, and has been deployed in a variety of attacking roles",
             category=category2)

session.add(item1)
session.commit()

item1 = Item(user_id=1, 
             name="Kerri Walsh Jennings",
             sex = "Female",
             country_id = 2,
             birthdate = date(1978, 8, 15),
             photo = "http://avp.com/wp-content/uploads/RS46180_NI4_6911-scr-e1457389328467-150x150.jpg",
             description= "Kerri Walsh Jennings attended Stanford University where she played volleyball. During her time at Stanford, Walsh was named a four-time first team All-American and won back-to-back National Championships in 1996 and 1997",
             category=category3)

session.add(item1)
session.commit()

item1 = Item(user_id=1, 
             name="Brooke Sweat",
             sex = "Female",
             country_id = 2,
             birthdate = date(1986, 3, 27),
             photo = "http://avp.com/wp-content/uploads/RS52753_DSC_3753-scr-150x150.jpg",
             description= "Brooke Sweat attended college at Flordia Gulf Coast University, where she played outside hitter. Sweat left FGCU as the career leader in kills and also recorded over 1000 kills and digs.",
             category=category3)

session.add(item1)
session.commit()
             
item1 = Item(user_id=1, 
             name="Brittany Hochevar",
             sex = "Female",
             country_id = 2,
             birthdate = date(1981, 5, 26),
             photo = "http://avp.com/wp-content/uploads/RS6371_130818_AVP_1103-scr-e1457389541837-150x150.jpg",
             description= "Hochevar spent her collegiate career at Long Beach State, where she replaced Misty May as their setter. As a senior, Hochevar was named an AVCA All-American as a setter. ",
             category=category3)

session.add(item1)
session.commit()

item1 = Item(user_id=1, 
             name="Phil Dalhausser",
             sex = "Male",
             country_id = 2,
             birthdate = date(1980, 1, 26),
             photo = "http://avp.com/wp-content/uploads/RS28169_KK2_7907-scr-e1457390010922-150x150.jpg",
             description= "Phil Dalhausser, aka The Thin Beast, was born in Baden, Switzerland.  He attended Mainland High School in Daytona Beach, FL, but did not start playing volleyball until his senior year.",
             category=category3)

session.add(item1)
session.commit()

item1 = Item(user_id=1, 
             name="Emily Day",
             sex = "Female",
             country_id = 2,
             birthdate = date(1987, 8, 9),
             photo = "http://avp.com/wp-content/uploads/RS50538_AVP_StPete_Sunday-29-scr-e1457653833257-150x150.jpg",
             description= "Emily Day attended school locally, at Loyola Marymount University, where she was a three time WCC All-Academic team member.",
             category=category3)

session.add(item1)
session.commit()

print "added items!"