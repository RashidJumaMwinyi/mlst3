import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import json
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")


@app.route("/get_cusine")
def get_cusine():
    cusines = mongo.db.cusines.find()
    return render_template("cusines.html", cusines=cusines)



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.user.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(
                request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for(
            "profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.user.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get(
                    "username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.user.find_one(
        {"username": session["user"]})["username"]
    return render_template("profile.html", username=username)


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))



@app.route("/add_cusine", methods = ["GET", "POST"])
def add_cusine():
    if request.method == "POST":
        task = {
            "category_name" : request.form.get("category_name"),
            "task_name" : request.form.get("task_name"),
            "task_description" : request.form.get("task_description"),
            "task_ingredients" : request.form.get("task_ingredients"),
            "created_by" : session["user"]
        }
        mongo.db.task.insert_one(task)
        flash("Cusine successfully Added")
        return redirect(url_for("get_cusine"))

    categories = mongo.db.category.find().sort("category_name", 1)
    return render_template("add_cusine.html", categories = categories)



@app.route("/edit_cusine/<cusine_id>", methods = ["GET", "POST"])
def edit_cusine(cusine_id):    
    cusine = mongo.db.cusines.find_one({"_id": ObjectId(cusine_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("edit_cusine.html",cusine=cusine, categories = categories)


# This render's an html file with a click on the home button labelled accordingly
@app.route("/pasta")
def pasta():
    with open("data/cusine.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("pasta.html",page_title="Pasta",cusine=data)


# This render's an html file with a click on the home button labelled accordingly
@app.route("/beef")
def beef():
    with open("data/cusine.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("beef.html",page_title="beef",cusine=data)


# This render's an html file with a click on the home button labelled accordingly
@app.route("/dessert")
def dessert():
    with open("data/cusine.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("dessert.html",page_title="dessert",cusine=data)



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
