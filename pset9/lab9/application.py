import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        #error message displayed in failure
        message = "Your input couldn't be accepted, reload and try again (name shouldnt have spaces)"


        # sanitize the data
        try:
            month = int(request.form.get("month"))
            day = int(request.form.get("day"))
        except:
            return render_template("failure.html", message=message)

        # we will assime that febrary 29 30 31 exists bc im lazy to implement it
        print(request.form.get("name"), request.form.get("name").isalpha())
        if not request.form.get("name").isalpha() or month < 1 or month > 12 or day < 1 or day > 31:
            return render_template("failure.html", message=message)

        # Add the user's entry into the database
        db.execute("REPLACE INTO birthdays (name, month, day) VALUES(?, ?, ?)", request.form.get("name"), month, day)

        return redirect("/")

    else:

        #  Display the entries in the database on index.html
        people = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", people=people)


@app.route("/delete", methods=["POST"])
def delete():

    name = request.form.get("name")
    print(name)
    if not name.isalpha():
        return render_template("failure.html", message="Not valid name, must be without number neither spaces")

    ans = db.execute("DELETE FROM birthdays WHERE name=?", name)
    print(ans)


    return redirect("/")