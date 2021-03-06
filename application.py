import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash
# this is csrf security extension
from flask.ext.seasurf import SeaSurf
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, Country, User
# New imports to enable logins with Oauth2 session tokens etc
# we use the as keyword here since we are already using session
# to describe our database session with sqlalchemy
from flask import session as login_session
# these will help generate a pseudo-random string to id each session
import random
import string
# this is a json method for storing client id and secrets
from oauth2client.client import flow_from_clientsecrets
# this method handles errors exchanging 1 time auth codes for access codes
from oauth2client.client import FlowExchangeError
# python http client library
import httplib2
# converts in memory objects to json objects
import json
# converts return value into a response to send to a client
from flask import make_response
# Apache urlrequests library - basically an improved urllib2
import requests
# python XML tree api & minidom to allow XML pretty printing
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

app = Flask(__name__)
# this uses the csrf security extension SeaSurf with app
csrf = SeaSurf(app)
CLIENT_ID = json.loads(
                open('client_secret.json', 'r').read())['web']['client_id']
# Connect to Database and create database session
engine = create_engine('sqlite:///sports.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # redirect if not logged in
        if 'username' not in login_session:
            flash('You must be logged in for this operation')
            return redirect(url_for('showLogin'))
        return f(*args, **kwargs)
    return decorated_function


def category_auth_required(f):
    @wraps(f)
    def decorated_function(category_id):
        # redirect to main page & flash unauthorized if user is not creator
#        category = session.query(Category).filter_by(id=category_id).one()
        category_to_work_on = session.query(Category).filter_by(id=category_id).one()
        # redirect to main page & flash unauthorized if user is not creator
        if not user_authorized(category_to_work_on.user_id, "delete"):
            return redirect(url_for('showCategories'))
        return f(category_to_work_on)
    return decorated_function


def item_auth_required(f):
    @wraps(f)
    def decorated_function(category_id, item_id):
        # redirect to main page & flash unauthorized if user is not creator
#        category = session.query(Category).filter_by(id=category_id).one()
        item_to_work_on = session.query(Item).filter_by(id=item_id).one()
        if not user_authorized(item_to_work_on.user_id, "delete"):
            return redirect(url_for('showCategories'))
        return f(category_id, item_to_work_on)
    return decorated_function


# this exempts this route from SeaSurf CSRF protection
# is it accurate that pre-login CSRF protection not needed since
# we can't take any protected actions until post login?  We are
# still doing verification of state token between client & server
# see https://discussions.udacity.com/t/p3-extracredt-seasurf/28739/16
@csrf.exempt
# verify client response token matches state token sent to client
# to avoid CSRF - gconnect is the post url we defined in the AJAX within
# our login template - could have called it something else
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code since we know state tokens match
    code = request.data
    try:
        # create an oauth_flow object with our client secret
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        # Exchange the authorization code for a credentials object from Google
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to exchange for authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    # that google url will return an error if invalid & token info otherwise
    result = json.loads(h.request(url, 'GET')[1])
    # print "**LOGIN RESULT: ", result
    # print "**ACCESS TOKEN: ", credentials.access_token
    # If there was an error in the access token info, abort.
    # NOTE: these result.get statements are parsing the json result object
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    # Store the access token in the session for later use.  A new token is
    # issued even if the user is already logged in
    login_session['access_token'] = credentials.access_token
    # Check to see if the user is already logged in and if so
    # return a 200 successful message but not reset all the login variables
    stored_credentials = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                 'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Whew! None of the above are true so store relevant info!
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    # store the google api userinfo response as answer
    answer = requests.get(userinfo_url, params=params)
    # convert the answer object to json and store as data.  Response defined here:
    # https://developers.google.com/+/web/api/rest/openidconnect/getOpenIdConnect#http-request
    data = answer.json()
    # access the relevant sections of data to store session info
    login_session['gplus_id'] = gplus_id
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'
    # check to see if the user is in the database & if not add a new user
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    # print "In LOGIN: Login Session Object: ", login_session
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# this exempts this route from SeaSurf CSRF protection
# is it accurate that pre-login CSRF protection not needed since
# we can't take any protected actions until post login?  We are
# still doing verification of state token between client & server
# see https://discussions.udacity.com/t/p3-extracredt-seasurf/28739/16
@csrf.exempt
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # get the short term access token
    # https://developers.facebook.com/docs/facebook-login/access-tokens
    access_token = request.data
    # print "access token received %s " % access_token
    # convert short term token to a long term token
    # https://developers.facebook.com/docs/facebook-login/access-tokens/expiration-and-extension
    app_id = json.loads(open('fb_client_secret.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secret.json', 'r').read())['web']['app_secret']
    url = ('https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}'
           .format(app_id, app_secret, access_token))
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # Use token to get user info from API
    # this doesn't seem to be used
    # userinfo_url = "https://graph.facebook.com/v2.5/me"
    # strip expire tag from access token
    token = result.split("&")[0]
    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]
    # The token must be stored in the login_session in order to properly logout,
    # let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token
    # Get user picture
    url = ('https://graph.facebook.com/v2.4/me/picture?{}&redirect=0&height=200&width=200'
           .format(token,))
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]
    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius: 150px;
               -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    flash("Now logged in as %s" % login_session['username'])
    return output


# generic disconnect function rather than individual gdisconnect & fbdisconnect
@app.route('/disconnect')
def disconnect():
    # print "In disconnect: Login Session Object: ", login_session
    access_token = login_session.get('access_token')
    # return an error if no one is logged in
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # load the url to revoke the access token on Google's servers
    if 'facebook_id' in login_session:
        facebook_id = login_session['facebook_id']
        url = ('https://graph.facebook.com/{}/permissions?access_token={}'
               .format(facebook_id, access_token))
        request_type = 'DELETE'
        # this is the index of the revoke response where the status code is
        result_index = 0
    else:
        # logged in thru google so disconnect there
        url = ('https://accounts.google.com/o/oauth2/revoke?token={}'
               .format(login_session['access_token'],))
        request_type = 'GET'
        result_index = 0
    h = httplib2.Http()
    result = h.request(url, request_type)
    # print loop and indexing result below rather than above for debug
    # for r in result:
        # print "**{} RESULT**: ".format(login_session['provider']), r
    result = result[result_index]
    if result['status'] == '200':
        print "CLEARING THE LOGIN SESSION"
        login_session.clear()
        print "Successfully disconnected, YOU ARE LOGGED OUT"
        flash('Successfully disconnected, YOU ARE LOGGED OUT')
        return redirect(url_for('showCategories'))
    else:
        response = make_response(json.dumps(
                       'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Create anti-forgery state token
# this is a 32 character pseudo-random mix of uppercase characters and digits
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    # this random string is store as state for the login session
    login_session['state'] = state
# THIS IS THE GOOGLE DOCUMENTATION PYTHON RECOMMENDATION
# BUT IT REQUIRES THE GOOGLE API PYTHON LIBRARY TO FUNCTION
# https://developers.google.com/identity/protocols/OpenIDConnect#server-flow
# Create a state token to prevent request forgery.
# Store it in the session for later validation.
#     state = hashlib.sha256(os.urandom(1024)).hexdigest()
#     session['state'] = state
# Set the client ID, token state, and application name in the HTML while
# serving it.
#     response = make_response(
#       render_template('index.html',
#                       CLIENT_ID=CLIENT_ID,
#                       STATE=state,
#                       APPLICATION_NAME=APPLICATION_NAME))
    return render_template('login.html', STATE=login_session['state'],
                           page_title="Login")


# JSON APIs to view Category Information
@app.route('/category/<int:category_id>/JSON')
@app.route('/category/<int:category_id>/item/JSON')
def categoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/category/<int:category_id>/item/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)


@app.route('/category/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


# XML endpoints
@app.route('/category/XML')
def categoriesXML():
    top = ET.Element('top')
    top.text = "Catalog Categories"
    categories = session.query(Category).all()
    for c in categories:
        category = ET.SubElement(top, 'category')
        dict = c.serialize
        for k in c.serialize:
            subelement = ET.SubElement(category, k)
            subelement.text = str(dict[k])
        xml = escape("<?xml version='1.0'?>" + ET.tostring(top, 'utf-8'))
    return xml


@app.route('/category/<int:category_id>/item/<int:item_id>/XML')
def itemXML(category_id, item_id):
    top = ET.Element('top')
    top.text = "Item Detail"
    item = session.query(Item).filter_by(id=item_id).one()
    i = ET.SubElement(top, 'item')
    dict = item.serialize
    for k in dict:
        subelement = ET.SubElement(i, k)
        subelement.text = str(dict[k])
    xml = escape("<?xml version='1.0'?>" + ET.tostring(top, 'utf-8'))
    return xml


@app.route('/category/<int:category_id>/XML')
@app.route('/category/<int:category_id>/item/XML')
def categoryXML(category_id):
    top = ET.Element('top')
    top.text = "Category items"
    category = session.query(Category).filter_by(id=category_id).one()
    cat = ET.SubElement(top, 'category')
    cat_name = ET.SubElement(cat, 'name')
    cat_name.text = category.name
    for item in category.items:
        i = ET.SubElement(top, 'item')
        dict = item.serialize
        for k in dict:
            subelement = ET.SubElement(i, k)
            subelement.text = str(dict[k])
        xml = escape("<?xml version='1.0'?>" + ET.tostring(top, 'utf-8'))
    return xml


# Show all categories
@app.route('/')
@app.route('/category/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    #print "Category Login Session Object: ", login_session
    latest = getLatestThree()
    # show the public template if not logged in (no add category option)
    if 'username' not in login_session:
        return render_template('categories.html', auth=False, latest=latest,
                               page_title="Categories", categories=categories)
    else:
        return render_template('categories.html', auth=True, latest=latest,
                               page_title="Categories", categories=categories)


# Create a new category
@app.route('/category/new/', methods=['GET', 'POST'])
@login_required
def newCategory():
    # redirect if not logged in
#     if 'username' not in login_session:
#         return redirect(url_for('showLogin'))
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'],
                               icon=request.form['icon'],
                               user_id=login_session['user_id'])
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html', page_title="New Category")


# Edit a category
@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
@login_required
@category_auth_required
def editCategory(category):
# redirect if not logged in
#     if 'username' not in login_session:
#         return redirect(url_for('showLogin'))
#     editedCategory = session.query(Category).filter_by(id=category_id).one()
# redirect to main page & flash unauthorized if user is not creator
#     if not user_authorized(editedCategory.user_id, "edit"):
#         return redirect(url_for('showCategories'))
    if request.method == 'POST':
        if request.form['name']:
            category.name = request.form['name']
        if request.form['icon']:
            category.icon = request.form['icon']
        flash('Category Successfully Edited %s' % category.name)
        return redirect(url_for('showCategories'))
    else:
        return render_template('editCategory.html', category=category,
                               page_title="Edit Category")


# Delete a category
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
@login_required
@category_auth_required
def deleteCategory(category):
    # redirect if not logged in
#     if 'username' not in login_session:
#         return redirect(url_for('showLogin'))
#     categoryToDelete = session.query(Category).filter_by(id=categoryid).one()
#     # redirect to main page & flash unauthorized if user is not creator
#     if not user_authorized(categoryToDelete.user_id, "delete"):
#         return redirect(url_for('showCategories'))
    if request.method == 'POST':
        session.delete(category)
        flash('%s Successfully Deleted' % category.name)
        session.commit()
        return redirect(url_for('showCategories', category_id=category.id))
    else:
        return render_template('deleteCategory.html', category=category,
                               page_title="Delete Category")


# Show a category's items
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/item/')
def showItem(category_id):
    # print "Item Login Session Object: ", login_session
    category = session.query(Category).filter_by(id=category_id).one()
    creator = category.user
    # we use get here since it returns null vs an exception if
    # login_session is empty
    if login_session.get("user_id") == creator.id:
        return render_template('item.html', auth=True, category=category,
                               creator=creator)
    else:
        return render_template('item.html', auth=False,
                               category=category, creator=creator)



@app.route('/category/<int:category_id>/item/<int:item_id>')
def showItemDetail(category_id, item_id):
    # print "Item Login Session Object: ", login_session
    item = session.query(Item).filter_by(id=item_id).one()
    age = getAge(item.birthdate)
    creator = item.category.user
    # redirect if user manually entered incorrect category/item url
    if category_id != item.category.id:
        flash('No such item in that category')
        return redirect(url_for('showCategories'))
    # we use get here since it returns null vs an exception if
    # login_session is empty
    if login_session.get("user_id") == creator.id:
        return render_template('item_detail.html', item=item, auth = True,
                               category=item.category, creator=creator, age=age)    
    else:
        return render_template('item_detail.html', item=item, auth = False,
                               category=item.category, creator=creator, age=age)



# Create a new item
@app.route('/category/<int:category_id>/item/new/', methods=['GET', 'POST'])
@login_required
@category_auth_required
def newItem(category):
    if request.method == 'POST':
        bday = request.form['birthdate']
        if bday:
            bday = datetime.datetime.strptime(bday, "%Y-%m-%d").date()
            newItem = Item(name=request.form['name'],
                           description=request.form['description'],
                           sex=request.form['sex'],
                           photo=request.form['photo'],
                           country_id=request.form['country_id'],
                           category_id=category.id, birthdate=bday,
                           user_id=login_session['user_id'])
        else:
            newItem = Item(name=request.form['name'],
                           description=request.form['description'],
                           sex=request.form['sex'],
                           photo=request.form['photo'],
                           country_id=request.form['country_id'],
                           category_id=category.id,
                           user_id=login_session['user_id'])
            session.add(newItem)
            session.commit()
            flash('New Item %s Item Successfully Created' % (newItem.name))
            return redirect(url_for('showItem', category_id=category.id))
    else:
        return render_template('newitem.html', category_id=category.id,
                               countries=getCountryInfo(),
                               page_title="Add An Item")


# Edit an item
@app.route('/category/<int:category_id>/item/<int:item_id>/edit',
           methods=['GET', 'POST'])
@login_required
@item_auth_required
def editItem(category_id, editedItem):
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['photo']:
            editedItem.photo = request.form['photo']
        if request.form['country_id']:
            editedItem.country_id = request.form['country_id']
        if request.form['sex']:
            editedItem.sex = request.form['sex']
        if request.form['birthdate'] and request.form['birthdate'] != "None":
            try:
                editedItem.birthdate = datetime.datetime.strptime(
                    request.form['birthdate'], "%Y-%m-%d").date()
            except ValueError:
                # print "Birthdate type: ", type(request.form['birthdate'])
                flash('Incorrect date format.  Please use the requested format')
                return render_template('edititem.html', category_id=category_id,
                                       item=editedItem,
                                       countries=getCountryInfo(),
                                       page_title="Edit Item")

        session.add(editedItem)
        session.commit()
        flash('Item Successfully Edited')
        return redirect(url_for('showItem', category_id=category_id))
    else:
        return render_template('edititem.html', category_id=category_id,
                               item=editedItem,
                               countries=getCountryInfo(),
                               page_title="Edit Item")


# Delete an item
@app.route('/category/<int:category_id>/item/<int:item_id>/delete',
           methods=['GET', 'POST'])
@login_required
@item_auth_required
def deleteItem(category_id, item):
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showItem', category_id=category_id))
    else:
        return render_template('deleteItem.html', category_id=category_id,
                               item=item, page_title="Delete Item")


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=login_session['email']).one()
        return user.id
    except:
        return


def createUser(login_session):
    # create a new user and return the user id
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    return getUserID(login_session['email'])



def user_authorized(id_to_check_against, text):
    # checks logged in user vs input id and adds text to flash message if not
    # CHORE: should I just redirect to main page from here?  Currently left
    #        flexible with redirect outside the function
    if id_to_check_against != login_session['user_id']:
        flash('''Only the category owner is authorized to {}.  You have been
                 redirected to the main page.'''.format(text))
        return False
    return True


def getCountryInfo(country_ids=None):
    # return a dictionary of country_id: countrynames, flags) given a
    # list of country_ids.  Return all Country objects if no list is provided.
    countries = {}
    if country_ids:
        for id in country_ids:
            countries[id] = session.query(Country.name,
                                          Country.flag).filter_by(id=id).one()
    else:
        all_countries = session.query(Country).all()
        for c in all_countries:
            countries[c.id] = (c.name, c.flag)
    return countries


def getAge(bday):
    today = datetime.date.today()
    try:
        return (today.year - bday.year
                - ((today.month, today.day)< (bday.month, bday.day)))
    except:
        return "TBD"


def getLatestThree():
    latest = (session.query(Item.id, Item.name, Category.name, Category.id)
        .join(Category)
        .order_by(Item.id.desc()).limit(3).all())
    return latest


            

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
