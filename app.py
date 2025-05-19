from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
# Import for Migrations

from flask_migrate import Migrate, migrate
from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import and_, or_, not_
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy import Index
from sqlalchemy import create_engine
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Create an index

app = Flask(__name__)
load_dotenv()
CORS(app)
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

# Configuring SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class sale(db.Model):
    """User Model

    Args:
        db (_type_): Model from SQL Alchemy

    Returns:
        string: Only check_password returns, else used to store user info
    """
    __tablename__ = "sale"
    username = db.Column(db.String(150), primary_key = True, nullable=False, index = True)
    itemname = db.Column(db.String(150), primary_key = True, nullable = False)
    itemprice = db.Column(db.String(150), nullable = False, index = True)
    #Index("index1", "itemprice")
    #Index("index2", "username")

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('frontpage.html')

@app.route('/sell', methods=['GET', 'POST']) 
def s():
    return render_template('sell.html')

@app.route('/edit', methods=['GET', 'POST']) 
def e():
    return render_template('edit.html')

@app.route('/delete', methods=['GET', 'POST']) 
def d():
    return render_template('delete.html')

@app.route('/buy', methods=['GET', 'POST']) 
def b():
    return render_template('buy.html')

@app.route('/view', methods=['GET', 'POST']) 
def v():
    return render_template('view.html')

@app.route('/viewforreal', methods=['GET', 'POST']) 
def show_view():
    username = request.form['username']
    row = sale.query.filter(username == sale.username)
    return render_template('showview.html', row=row)

@app.route('/display_edit', methods=['GET', 'POST']) 
def resde():
    username = request.form['username']
    itemname = request.form['old']
    newprice = request.form['new']
    stmt = (
    update(sale).
        where(and_(sale.username == username, sale.itemname == itemname))
        .values(itemprice = newprice)
    )
    db.session.execute(stmt)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/display_sell', methods=['GET', 'POST'])
def sell_to_home():
     username = request.form['username']
     item_name = request.form['item name']
     item_price = request.form['item price']
     new_item = sale(username = username, itemname = item_name, itemprice = item_price)
     db.session.add(new_item)
     db.session.commit()
     return redirect('/')

@app.route('/display_delete', methods=['GET', 'POST'])
def delete_to_home():
    username = request.form['username']
    name = request.form['name']
    stmt = delete(sale).where(and_(sale.itemname == name, sale.username==username))
    db.session.execute(stmt)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/process_buy', methods=['GET', 'POST']) 
def filter():
    minprice = request.form['min price']
    rows = sale.query.filter(sale.itemprice >= minprice)
    return render_template('show_results.html', rows=rows)

if __name__ in '__main__':
    # Create a db and table
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.run(port = "8080", debug=True)
