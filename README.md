# [Catalog Project](https://www.udacity.com/course/viewer#!/c-ud197-nd/l-3521918727/m-3519689284)

This project is a python module using SQLAlchemy as the ORM with a PostgreSQL database which creates a simple catalog app with categories and items.  It incorporates 3rd party authentication with Google and Facebook and each category uses authorization to allow only the category creator to edit the category and add items.  The SeaSurf extension is used for CSRF protection.  For this project, I chose to make the catalog categories sports and the items players.  The site uses a basic responsive grid & components from Bootstrap.  JSON & XML endpoints are provided for categories(sports), category items(players), and individual items(players).  The 3 most recently added players and their sports are displayed on the main page.  Graphics for each sport are from the Rio 2016 Olympics and player photos are from respective professional organizations or ESPN.  All graphics are for demonstration purposes only and are the property of their respective owners.



## Table of contents

* [Quick start](#quick-start)
* [Bugs and feature requests](#bugs-and-feature-requests)
* [Documentation](#documentation)
* [Contributing](#contributing)
* [Community](#community)
* [Versioning](#versioning)
* [Creators](#creators)
* [Copyright and license](#copyright-and-license)


## Quick start

To get started:

* This project requires python 2.7
* Clone the repo: git clone https://github.com/thatkahunaguy/Sports-catalog.git
* Add client secret files which have not been included in the repo: client_secret.json & fb_client_secret.json  [see notes on project submission for where to find these]
* To run the program, at the command prompt type: python application.py
* Navigate to localhost:5000 to view the site
* To create your own categories and items you must login (upper right corner)
* To login you must have a Google or Facebook account
* Once you are logged in you can create a category from the main page and items from within the category
* The python modules are described below
* Note: the populated databse sports.db is included in the repo.  If it fails for some reason you can create and repopulate the database by delecting sports.db and typing "python populate_sports.py" at the command prompt.

### What's included

Within the download you'll find the following directories and files. You'll see the folowing:

```
tournament/
├── application.py       *the main catalog application*
├── populate_sports.py   *database population file with various sports & players*
├── database_setup.py    *SQLAlchemy database setup file*
├── sports.db            *initial database - this can be deleted and repopulated if needed*
├── static               *css styles and static resources*
├── templates            *html templates and partials*
├── README.md
```
NOTE: Client secret files(client_secret.json for Google and fb_client_secret.json for Facebook) are not included and must be added to the directory


## Bugs and feature requests
* Currently player countries and country flags can only be pre-populated in the database as the program doesn't provide a CRUD interface for this.  Simple enough to add but time to move on.
* The program doesn't currently include token renewal after expiration for third party authentication with Google and Facebook.  Users must currently login again after token expiration.

## Documentation

##### Login/Authentication

Users can login with either Google or Facebook accounts.  Information in the database can be viewed without logging in but CRUD actions for categories(sports) and items(players) can only be performed after logging in.

##### Authorization
Only the creator of a category(sport) is authorized to create, edit, or delete items(players) within a category.

##### Categories(Sports)
Sports are the categories in the catalog as currently populated.  Each category can have a name and a photo/icon url associated with it.  In the case of the prepopulated sports these images are from the Rio 2016 Olympics.  On the main page which displays categories, the most recent 3 items(players) added to the database along with their sports are displayed.

##### Items(Players)
Players are the items in the catalog as currently populated.  Each player has fields for a name, category(sport), country, birthdate, photo url, and description/bio.  5 countries are prepopulated in the database(no CRUD interface currently provided) along with their flags and are selected when adding or entering a player.  The players age is displayed based on the birthdate provided.  If the birthdate is not provided, TBD is shown for the age.

##### JSON & XML Endpoints
JSON & XML endpoints are provided for:
* categories(sports): http://localhost:5000/category/JSON or XML
* category items(players): http://localhost:5000/category/#/item/JSON or XML
* individual items(players): http://localhost:5000/category/#/item/#/JSON or XML
modify the last element of the url accordingly for JSON or XML

## Contributing

This site uses [Bootstrap](http://getbootstrap.com) although in hindsite some simple CSS would have sufficed :)

Images are for demonstration purposes only and are copyright of their respective owners [ATP](http://www.atpworldtour.com), [WTA](http://www.wtatennis.com), [Rio 2016](http://www.rio2016.com), [AVP](http://www.avp.com), & [ESPNFC](http://www.espnfc.com). 

## Community

* Udacity discussions are [here](https://discussions.udacity.com/c/nd004-p3-item-catalog).


## Versioning

Debut release

## Creators

**John Glancy**

* <https://github.com/thatkahunaguy>

**Udacity**
* <https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004>

## Copyright and license

Code released under [the MIT license](https://opensource.org/licenses/MIT). Docs released under [Creative Commons](http://creativecommons.org/licenses/by/4.0/).


