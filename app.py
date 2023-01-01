# see design.md for citations on where i found how to code some of this!

# import libraries
import json
import os
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from helpers import login_required, getUser, get_google_provider_cfg, inBerg,sortFunction
from flask_login import LoginManager
from oauthlib.oauth2 import WebApplicationClient
from flask_mail import Mail, Message
import requests

# database
db = SQL("sqlite:///final.db")

# get google info via command line

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", None)
MAP_KEY = os.environ.get("MAP_KEY", None)



# configure application
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_COOKIE_NAME"] = "session"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'eatinberg@gmail.com'
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail= Mail(app)


# configure login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return getUser(user_id)

# configure google client
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# cache stuff
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# index page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        if session.get("user_id") is None:
            return render_template("unlogged.html")
        else:
            profile_pic = db.execute("SELECT profile_pic FROM user WHERE id = ?", session["user_id"])[0]["profile_pic"]
            link = "https://maps.googleapis.com/maps/api/js?key="+MAP_KEY+"&callback=myMap"
            print(link)
            return render_template("get_data.html", profile_pic = profile_pic, link = link)
    else:
        # from ajax request that gets and send latitude and longitude
        location = json.loads(request.get_json())
        lat =  float(location["latitude"])
        long = float(location["longitude"])
        db.execute("UPDATE user SET latitude = ?, longitude = ? WHERE id = ? ", lat,long,session["user_id"])
        return "Done"


# login
@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    # get authorization endpoint
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # where to redirect
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

# after login page
@app.route("/login/callback")
def callback():
    # code from google
    code = request.args.get("code")

    # where to get tokens
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # parse tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    # get profile info with tokens
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # get info
    unique_id = userinfo_response.json()["sub"]
    users_email = userinfo_response.json()["email"]
    picture = userinfo_response.json()["picture"]
    users_name = userinfo_response.json()["name"]
    friends = {"keys" :["1", "2"]}

    # if new user add to user db
    if not db.execute("SELECT * FROM user WHERE id = ?", unique_id):
          db.execute( "INSERT INTO user (id, name, email, profile_pic, friends) VALUES (?, ?, ?, ?, ?)", unique_id, users_name, users_email, picture, json.dumps(friends))

    # clear session then login
    session.clear()
    session["user_id"] = unique_id

    # redirect to index
    return redirect("/")

# logout
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

@app.route("/map",  methods=["GET", "POST"])
@login_required
def map():
    if request.method == "GET":
        # get details about location and user
        currentMode = db.execute("SELECT ghost FROM user WHERE id = ?", session["user_id"])[0]["ghost"]
        lat = float(db.execute("SELECT latitude FROM user WHERE id = ?", session["user_id"])[0]["latitude"])
        long = float(db.execute("SELECT longitude FROM user WHERE id = ?", session["user_id"])[0]["longitude"])
        berg = inBerg(lat,long, currentMode)
        profile_pic = db.execute("SELECT profile_pic FROM user WHERE id = ?", session["user_id"])[0]["profile_pic"]
        name = db.execute("SELECT name FROM user WHERE id = ?", session["user_id"])[0]["name"]

        return render_template("map.html", lat = lat, long = long, inBerg = berg, profile_pic = profile_pic, name = name, mode = currentMode)
    else:
        # post happens when someone switches to ghost mode...
        ghost = request.form.get("ghost")
        # toggle ghost mode
        if ghost:
            db.execute("UPDATE user SET ghost = 1 where id = ?", session["user_id"])
        else:
            db.execute("UPDATE user SET ghost = 0 where id = ?", session["user_id"])


        return redirect("/map")


@app.route("/friends", methods=["GET", "POST"])
@login_required
def friends():
    if request.method == "GET":
        # get info from session
        if session.get("hidden") is None:
            hidden = ""
        else:
            hidden = session["hidden"]
        if session.get("email") is None:
            email = ""
        else:
            email = session["email"]
        session["hidden"] = ""
        session["email"] = ""

        # get user info
        info = db.execute("SELECT friends from user where id = ?",session["user_id"])[0]["friends"]
        info = json.loads(info)["keys"]
        profile_pic = db.execute("SELECT profile_pic FROM user WHERE id = ?", session["user_id"])[0]["profile_pic"]

        # save info about friends
        friends = []
        if (type(info) is str):
            # get friends details and put in list
            deets = db.execute("SELECT * from user where id = ?", info)[0]
            currentMode = db.execute("SELECT ghost FROM user WHERE id = ?", info)[0]["ghost"]
            berg = inBerg(deets["latitude"], deets["longitude"],currentMode)
            if berg:
                deets["inBerg"] = "IN BERG"
            else:
                deets["inBerg"] = "NOT IN BERG"
            friends.append(deets)
        else:
            for key in info:
                # get friends details and put in list
                deets = db.execute("SELECT * from user where id = ?", key)[0]
                currentMode = db.execute("SELECT ghost FROM user WHERE id = ?", key)[0]["ghost"]
                berg = inBerg(deets["latitude"], deets["longitude"],currentMode)
                if berg:
                    deets["inBerg"] = "IN BERG"
                else:
                    deets["inBerg"] = "NOT IN BERG"
                friends.append(deets)

        friends.sort(key=sortFunction)
        return render_template("friends.html", friends = friends, hidden = hidden,email=email, profile_pic = profile_pic)
    else:
        # post happens when adding a friend
        # get info
        email = request.form.get("email").lower().lstrip().rstrip()
        id = db.execute("SELECT id FROM user WHERE email = ?", email)
        info = db.execute("SELECT friends from user where id = ?",session["user_id"])[0]["friends"]
        info = json.loads(info)["keys"]
        # if the user has no account
        if not id:
            session["hidden"] = "Unfortunately, '" + email + "' does not have an account on Eat-In-Berg. Please add a new friend or invite them to join!"
            session["email"] = email
            return redirect("/friends")
        id = id[0]["id"]
        # if already friends with user
        if (info == id) or (id in info):
            session["hidden"] = "You are already friends with '" + email +"'!"
            return redirect("/friends")
        # otherwise, add user to friends JSON
        info.append(id)
        holder = "UPDATE user SET friends =  json_insert(' { " + '"' + "a" + '"' + ": 1 } ', '$.keys', json_array("
        for i in info:
            holder += '"'+ i + '"' + ","
        holder = holder[:-1]
        holder += ") ) where id = ?"
        db.execute(holder, session["user_id"])
        session["hidden"] = "Successfully added '" + email +"'!"
        return redirect("/friends")

@app.route("/delete", methods=["POST"])
@login_required
def delete():
    # get info about who to delete
    id = request.form.get("id")
    id = str(id)
    info = db.execute("SELECT friends from user where id = ?",session["user_id"])[0]["friends"]
    info = json.loads(info)["keys"]
    info.remove(id)
    holder = "UPDATE user SET friends =  json_insert(' { " + '"' + "a" + '"' + ": 1 } ', '$.keys', json_array("
    for i in info:
        holder += '"'+ i + '"' + ","
    holder = holder[:-1]
    holder += ") ) where id = ?"
    # remove that person
    db.execute(holder, session["user_id"])
    return redirect("/friends")

@app.route("/sendEmail", methods=["POST"])
@login_required
def sendEmail():
    # get details about who is sending and getting email
    email = request.form.get("email")
    rec = []
    rec.append(email)
    name = db.execute("SELECT name from user where id = ?",session["user_id"])[0]["name"]

    # format and send email
    msg = Message('Join Eat-In-Berg!', sender = 'eatinberg@gmail.com', recipients = rec)
    msg.html = "Hello! <br> " + name + " would like to share whether they are in Berg with you! Accept them by creating an account on <a href='https://127.0.0.1:5000/'> Eat-In-Berg </a> <br> Have a great day!"
    mail.send(msg)

    #show succsessful
    session["hidden"] = "'" + email + "' has been invited!"

    return redirect("/friends")

# run program
if __name__ == "__main__":
    app.run(ssl_context="adhoc")
