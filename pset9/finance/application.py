import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from datetime import datetime
import pytz
# need date to store the second of the purchase

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    owned = db.execute("SELECT symbol, quantity FROM owned WHERE user_id=?", session["user_id"])
    owned_dict_list = []

    # the query returns a list of dicts, remember?
    # now i'm creating the list i want to input later
    for row in owned:
        print(row)
        quote = lookup(row["symbol"])
        if quote == None:
            return apology("I'm a cute little kitten", 418)

        # i want to modify this bc i want to pass it later, this is the easiest way
        quote['shares'] = row["quantity"]
        quote["total"] = row["quantity"] * quote["price"]
        owned_dict_list.append(quote)

    # appending last
    cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
    owned_dict_list.append({"name": "CASH", "symbol": "",  "shares": "", "price": "", "total": cash})

    # sum of everything
    # pass this alone bc easier for footer in index.html
    total = 0
    for rom in owned_dict_list:
        total += rom["total"]

    footer = {"symbol": "", "name": "", "shares": "", "price": "", "total": total}
    return render_template("index.html", owned=owned_dict_list, footer=footer)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # check if input is good
        if not request.form.get("shares") or not request.form.get("symbol"):
            return apology("shares or symbol could not be left blank")

        quote = lookup(request.form.get("symbol").upper())
        if quote == None:
            return apology("This symbol does not exist")

        try:
            shares = int(request.form.get("shares"))

            if shares < 0:
                raise
        except:
            return apology("You can't input not numeric characters for the shares!")

        try:
            db.execute("BEGIN TRANSACTION")
        except Exception as e:
            print(e)
            return apology("Couldn't create the transaction, lazy boy")
        # check if you can buy these
        user_id = session["user_id"]
        capital = db.execute("SELECT cash FROM users WHERE id=?", user_id)[0]["cash"]
        if capital < shares * quote["price"]:
            return apology("Not enough capital!")
        else:
            capital -= shares * quote["price"]

        # register the transaction
        tz_London = pytz.timezone('Europe/London')
        datetime_London = datetime.now(tz_London)
        date = datetime_London.strftime("%d/%m/%Y %H:%M:%S")
        try:
            db.execute("INSERT INTO trades (user_id, symbol, quantity, price, date) VALUES(?, ?, ?, ?,?)",
                       user_id, quote["symbol"], shares, quote["price"], date)
        # print(success) # here is the ID of the stuff i inputted
        except Exception as e:
            print(e)
            return apology("Couldn't create the transaction")

        # update quantity of owned shares and update capital
        # but first let me parse the output i get for currently_owned
        try:
            currently_owned = db.execute("SELECT quantity FROM owned WHERE user_id=? AND symbol=?", user_id, quote["symbol"])
        except Exception as e:
            print(e)
            return apology("something went wrong when i tried to get ya... No idea", 500)
        # i want list of dictsssss
        if len(currently_owned) == 0:
            currently_owned.append({"quantity": 0})

        # beginning the update!
        if not currently_owned[0]["quantity"]:
            try:
                # here if i can update the first and not the second...
                # i would get in a big mess bc basically u get them for free
                # but this is just a mockup and im lazy so i won't fix it.

                # no think now with commit transaction i can overcome this bug, and everything would be just fine.
                # yeeees it works fine, i used
                # db.execute("UPDATE users SET cash=? WHERE user_id=?", capital, user_id) wrong query (as user_id doens't exist, for debuggind this thing)
                db.execute("INSERT INTO owned (user_id, symbol, quantity) VALUES(?,?,?)", user_id, quote["symbol"], shares)
                db.execute("UPDATE users SET cash=? WHERE id=?", capital, user_id)

            # checking if it went fine
            except Exception as e:
                print(e)
                return apology("Could not set the quantity of shares or new capital", 500)
        else:
            try:
                db.execute("UPDATE owned SET quantity=? WHERE user_id=? AND symbol=?",
                           currently_owned[0]["quantity"] + shares, user_id, quote["symbol"])
                db.execute("UPDATE users SET cash=? WHERE id=?", capital, user_id)

            # same as before
            except Exception as e:
                print(e)
                return apology("Could not update the new quantity of shares or new capital", 500)

        try:
            db.execute("COMMIT")
        except Exception as e:
            print(e)
            return apology("Could not commit the transaction, don't know why (eheh i know i should know it, but i don't lol)", 500)

        # if everything went fine just redirect to home
        flash("Sussess! You bough it!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    try:
        # i want to see only my transactions!
        history = db.execute("SELECT symbol, quantity, price, date FROM trades WHERE user_id=? ORDER BY date", session["user_id"])
    except Exception as e:
        print(e)
        return apology("Lalala, history is past, don't think about it, it has passed")

    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # sanitize request args
        if len(request.form.get("symbol")) == 0:
            return apology("Can't enter null symbol")

        lookups = lookup(request.form.get("symbol").upper())
        if lookups == None:
            return apology("Coundn't request the quote")

        return render_template("quotes.html", lookups=lookups)
    else:

        # template form asking for quotes
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        password_repeat = request.form.get("confirmation")

        # doing some sanitization
        if password != password_repeat:
            return apology("The passwords do not match")

        if len(username) == 0:
            return apology("Username field is blank")
        elif len(password) == 0:
            return apology("Password field is blank, i'm angry now")

        # checking if there is same username in db
        is_same_username = db.execute("SELECT * FROM users WHERE username = ?", username)
        if (is_same_username):
            return apology("The username is taken, i'm sorry")

        # if not i can add new account
        else:
            success = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))
            if not success:
                return apology("Couldn't create the account")

        # mi logga così?
        login()
        # redirecting to home after finishing the registration
        return redirect("/")

    # i want to register, then just print the view
    else:
        return render_template("register.html")


# i don't know how useful it is to be able to change password
# while logged, but here it is
@app.route("/password", methods=["GET", "POST"])
@login_required
def password():

    if request.method == "POST":

        password = request.form.get("password")
        password_repeat = request.form.get("confirmation")

        # doing some sanitization
        if password != password_repeat:
            return apology("The passwords do not match")

        if len(password) == 0:
            return apology("Password field is blank, i'm angry now")

        success = db.execute("UPDATE users SET hash=? WHERE id=?", generate_password_hash(password), session["user_id"])
        if not success:
            return apology("Couldn't create the account")

        flash("You password has been successfully changed")
        # redirecting to home after finishing the registration
        return redirect("/")

    # i want to register, then just print the view
    else:
        return render_template("password.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        # check if input is good
        if not request.form.get("shares") or not request.form.get("symbol"):
            return apology("shares or symbol could not be left blank")

        quote = lookup(request.form.get("symbol").upper())
        if quote == None:
            return apology("This symbol does not exist")

        # i think i should put after begin transaction also this stuff... but im lazy?!
        # nooo im not lazy, i did this now ,see?
        try:
            db.execute("BEGIN TRANSACTION")
        except Exception as e:
            print(e)
            return apology("Couldn't create the transaction, lazy boy")

        # checking valid shares
        try:
            shares = int(request.form.get("shares"))
            owned_shares = db.execute("SELECT quantity FROM owned WHERE user_id=? AND symbol=?",
                                      session["user_id"], quote["symbol"])[0]["quantity"]
            if shares < 0 or shares > owned_shares:
                raise
        except:
            return apology("Invalid shares!")

        # update shares so i know this is a sell, and i reuse last part of buy
        shares = -shares

        # check if you can buy these
        user_id = session["user_id"]
        try:
            capital = db.execute("SELECT cash FROM users WHERE id=?", user_id)[0]["cash"]
        except Exception as e:
            print(e)
            return apology("couldn't check me, me bad, me badboy")
        capital -= shares * quote["price"]

        # register the transaction
        tz_London = pytz.timezone('Europe/London')
        datetime_London = datetime.now(tz_London)
        date = datetime_London.strftime("%d/%m/%Y %H:%M:%S")
        try:
            db.execute("INSERT INTO trades (user_id, symbol, quantity, price, date) VALUES(?, ?, ?, ?,?)",
                       user_id, quote["symbol"], shares, quote["price"], date)

        # print(success) # here is the ID of the stuff i inputted
        except Exception as e:
            print(e)
            return apology("Couldn't create the transaction")

        # update quantity of owned shares and update capital
        try:
            db.execute("UPDATE owned SET quantity=? WHERE user_id=? AND symbol=?", owned_shares + shares, user_id, quote["symbol"])
            db.execute("UPDATE users SET cash=? WHERE id=?", capital, user_id)

        # dunno why i put the comment here
        except Exception as e:
            print(e)
            return apology("Could not update the new quantity of shares or new capital", 500)

        try:
            db.execute("COMMIT")
        except Exception as e:
            print(e)
            return apology("Could not commit the transaction, don't know why (eheh i know i should know it, but i don't lol)", 500)

        # if everything went fine just redirect to home
        flash("Sussess! You sold it!")
        return redirect("/")

    else:

        # i'm only fetching the stuff i have, so front end is a little nicer
        try:
            tmp = db.execute("SELECT symbol FROM owned WHERE user_id=? AND quantity>0", session["user_id"])
        except Exception as e:
            print(e)
            return apology("Bruh i'm tired to write apologies just .... vai a quel paese <3", 500)

        owned = []
        for row in tmp:
            owned.append(row["symbol"])

        return render_template("sell.html", owned=owned)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)