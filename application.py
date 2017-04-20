from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
from products import *
from flask.ext.hashing import Hashing
from functools import wraps
from flask_session import Session
from tempfile import gettempdir

engine = create_engine('sqlite:///users.db', echo=True)
engine_products = create_engine('sqlite:///products.db', echo = True)

app = Flask(__name__)
hashing = Hashing(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

Session1 = sessionmaker(bind=engine_products)
ses = Session1()
qproducts = ses.query(Products)
url = qproducts.first().product_image

Session2 = sessionmaker(bind=engine)
s = Session2()
quser = s.query(User)

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=["GET","POST"])
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    error = None
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username']).strip()
        POST_PASSWORD = str(request.form['password']).strip()

        query = s.query(User).filter(User.username.in_([POST_USERNAME]))
        user_exists = query.first()
        #checks for username

        if user_exists:
            #checks for hashedpassword
            hashedpassword = query.first().password

            if hashing.check_value(hashedpassword, POST_PASSWORD, salt='timothy'):
                # remember which user has logged in
                session["username"] = query.first().username
                return render_template('homeloggedin.html', product_image = url , product = qproducts.first().product_name, entry_fee = qproducts.first().entry_fee)

            else:
                error = 'wrong password!'
                return render_template('login.html', error = error)

        else:
            error = 'wrong username!'
            return render_template('login.html', error = error)

    else:
        return render_template('login.html', error = error)

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        POST_USERNAME = str(request.form['username']).strip()
        POST_PASSWORD = str(request.form['password']).strip()
        POST_VENMO = str(request.form['venmo']).strip()

        query = s.query(User).filter(User.username.in_([POST_USERNAME]))
        result = query.first()
        if not result:
            hashedpw = hashing.hash_value(POST_PASSWORD, salt='timothy')
            user = User(POST_USERNAME, hashedpw, POST_VENMO)
            s.add(user)
            s.commit()
            return render_template('login.html', error = error)
        else:
            error = "username already exists!"
            return render_template('register.html', error = error)
    else:
        return render_template('register.html')

@app.route("/homeloggedin", methods=["GET","POST"])
@login_required
def homeloggedin():
    return render_template('homeloggedin.html', product_image = url , product = qproducts.first().product_name, entry_fee = qproducts.first().entry_fee)

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return render_template('login.html')

@app.route("/dibs", methods=["GET","POST"])
@login_required
def dibs():
    return render_template("dibs.html", rows=quser, product_image=url)

@app.route("/bids", methods=["GET","POST"])
@login_required
def bids():
    if request.method == "POST":
        NEWBID = request.form['newbid'].strip()
        q = s.query(User).filter(User.username.in_([session["username"]]))
        q.first().bid = NEWBID
        s.commit()
        bid = str(q.first().bid)
        qu = s.query(func.sum(User.bid)).scalar()
        return render_template("dibs.html", rows=quser, product_image=url)

    else:
        q = s.query(User).filter(User.username.in_([session["username"]]))
        bid = q.first().bid
        entered = str(q.first().entrance)
        qu = s.query(func.sum(User.bid)).scalar()
        chance = int((bid/qu)*100)
        if entered == "1":
            return render_template("bids.html", rows=quser, product_image=url, userbid= bid, chance = chance)
        else:
            return render_template("processing.html")

if __name__ == "__main__":
    app.run()
