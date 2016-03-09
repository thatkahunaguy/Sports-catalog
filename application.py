from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
# allow summary function labeling for reference
from sqlalchemy.sql import label
 
from database_setup import Base, Category, Item

from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

def session_start(dbase):
    engine = create_engine(dbase)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()
    
# these @ items are decorators which apply to the defined funciton
# below them (HelloWorld).  In this case the decorators run the 
# function whenever the url route has the specified string at the end
# these are defined within Flask

# this adds a JSON endpoint for all the categories
@app.route('/categories/JSON')
def categorysJSON():
    session = session_start('sqlite:///catalog.db')
    categories = session.query(Category).all()
    session.close()
    return jsonify(category=[Category.serialize for category in categories])

# this adds a JSON endpoint for the entire item for a category
@app.route('/categories/<int:category_id>/item/JSON')
def categoryitemJSON(category_id):
    session = session_start('sqlite:///catalog.db')
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    session.close()
    return jsonify(items=[i.serialize for i in items])

# this adds a JSON endpoint for the one item item for a category
@app.route('/categories/<int:category_id>/item/<int:item_id>/JSON')
def itemsJSON(category_id, item_id):
    session = session_start('sqlite:///catalog.db')
    items = session.query(Item).filter(Item.id == item_id and 
        Item.category_id == category_id).one()
    session.close()
    return jsonify(items=items.serialize)

# end of JSON endpoints

@app.route('/')    
@app.route('/categories')
def categories():
    session = session_start('sqlite:///catalog.db')
    # check only the first category
    categories = session.query(Category).order_by(Category.name).all()
    session.close()
    # changed output to a render template & then template to styled template
    return render_template('categories.html', categories = categories)

@app.route('/categories/<int:category_id>')    
@app.route('/categories/<int:category_id>/item')
def items(category_id):
    session = session_start('sqlite:///catalog.db')
    # check only the first category
    category = session.query(Category).filter_by(id=category_id).first()
    item = session.query(Item).filter_by(category_id=category_id).all()
#     output = '<h2>item Items for: {} </h2>'.format(category.name)
#     for item in item:
#         output += "<h3>{}   {}</h3> r_id: {} <br>".format(item.name, Item.price, Item.category_id)
#         output += Item.description
#         output += '<br>'
    # once again example code just opens a session in main & never closes it
    # is this what should be done?
    session.close()
    # changed output to a render template & then template to styled template
    return render_template('item.html', category = category, items = item)

# Task 1: Create route for newitem function here

@app.route('/categories/<int:category_id>/item/new', methods = ['GET', 'POST'])
def newitem(category_id):
    if request.method == 'POST':
        session = session_start('sqlite:///catalog.db')
        new_item = item(name = request.form['name'], price = request.form['price'],
            course = request.form['course'], description = request.form['description'],
            category_id = "{}".format(category_id))
        # note: sql alchemy generates an error if I try to access the
        # new_item object after the session
        # CHORE: should i store name in a variable to so I flash AFTER successful commit?
        flash('{} added successfully!'.format(new_Item.name))
        session.add(new_item)
        session.commit()
        session.close()
        
        return redirect(url_for('items',category_id = category_id))
    else:
        return render_template('newItem.html', category_id = category_id)

@app.route('/categories/new', methods = ['GET', 'POST'])
def newcategory():
    if request.method == 'POST':
        session = session_start('sqlite:///catalog.db')
        new_category = category(name = request.form['name'])
        # note: sql alchemy generates an error if I try to access the
        # new_item object after the session
        # CHORE: should i store name in a variable to so I flash AFTER successful commit?
        flash('{} added successfully!'.format(new_Category.name))
        session.add(new_category)
        session.commit()
        session.close()
        
        return redirect(url_for('categories'))
    else:
        return render_template('newCategory.html')

# Task 2: Create route for edititem function here

@app.route('/categories/<int:category_id>/item/<int:item_id>/edit', methods = ['GET', 'POST'])
def edititem(category_id, item_id):
    session = session_start('sqlite:///catalog.db')
    item = session.query(Item).filter(Item.id == item_id and Item.category_id == category_id).one()
    if request.method == 'POST':
        Item.name =  request.form['name']
        Item.price = request.form['price']
        Item.description =  request.form['description']
        Item.course = request.form['course']
        # note: sql alchemy generates an error if I try to access the
        # new_item object after the session
        # CHORE: should i store name in a variable to so I flash AFTER successful commit?
        flash('{} edited successfully!'.format(item.name))
        session.add(item)
        session.commit()
        session.close()
        return redirect(url_for('items',category_id = category_id))
    else:
        return render_template('editItem.html', item = item)

@app.route('/categories/<int:category_id>/edit', methods = ['GET', 'POST'])
def editcategory(category_id):
    session = session_start('sqlite:///catalog.db')
    category = session.query(Category).filter(Category.id == category_id).one()
    if request.method == 'POST':
        Category.name =  request.form['name']
        # note: sql alchemy generates an error if I try to access the
        # new_item object after the session
        # CHORE: should i store name in a variable to so I flash AFTER successful commit?
        flash('{} edited successfully!'.format(category.name))
        session.add(category)
        session.commit()
        session.close()
        return redirect(url_for('categories'))
    else:
        return render_template('editCategory.html', category = category)

# Task 3: Create a route for deleteitem function here

@app.route('/categories/<int:category_id>/item/<int:item_id>/delete', methods = ['GET', 'POST'])
def deleteitem(category_id):
    session = session_start('sqlite:///catalog.db')
    item = session.query(Item).filter(Item.id == item_id and Item.category_id == category_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        session.close()
        flash('{} deleted successfully!'.format(item.name))
        return redirect(url_for('items',category_id = category_id))
    else:
        return render_template('deleteItem.html', item = item)

@app.route('/categories/<int:category_id>/delete', methods = ['GET', 'POST'])
def deletecategory(category_id):
    session = session_start('sqlite:///catalog.db')
    category = session.query(Category).filter(Category.id == category_id).one()
    if request.method == 'POST':
        session.delete(category)
        session.commit()
        session.close()
        flash('{} deleted successfully!'.format(category.name))
        return redirect(url_for('categories'))
    else:
        return render_template('deleteCategory.html', category = category)

if __name__ == '__main__':
    # need a key for sessions to use message flashing - real key would be secure
    # class doesn't cover python sessions so CHORE: check for reference
    app.secret_key = 'super_secret_key'
    # this mode reloads the server each time code is changed & provides browser debug
    # might be security issue if not on local host?? check this
    app.debug = True  # NEVER USE IN PRODUCTION
    # this tells vagrant to listen to port 5000 on all public IP addresses
    # the documentation seems to indicate 0.0.0.0 is a security risk?!?
    # since all public IPs are listened to & in debug arbitrary code will run
    # localhost(127.0.0.1) doesn't work so need to use this - is it vagrant??
    app.run(host='0.0.0.0', port=5000)