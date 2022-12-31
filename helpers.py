# import libraries
import requests
from cs50 import SQL
from flask import redirect, render_template, session
from functools import wraps
from flask_login import UserMixin
 
# declare global variables and objects
db = SQL("sqlite:///final.db")
SCOPES = 'https://mail.google.com/'
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

# functions!

def get_google_provider_cfg():
    # return json of url
    return requests.get(GOOGLE_DISCOVERY_URL).json()

def inBerg(lat, long, mode):
    # berg coords
    berg_top_lat =  42.376174
    berg_bottom_lat = 42.375693
    berg_left_long = -71.115653
    berg_right_long = -71.115000

    # if on ghost mode
    if mode == 1:
        return False

    # if don't know location
    if not lat or not long:
        return False

    # if inside berg
    if ((long >= berg_left_long) and (long <= berg_right_long) and (lat >= berg_bottom_lat ) and (lat <= berg_top_lat)):
        return True
    
    else:
        return False

def sortFunction(info):
    # allows sort
    return info["inBerg"]
   
def login_required(f):
    # requires login
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function
        
def getUser(user_id):
    # gets user using sql
    user = db.execute("SELECT * FROM user WHERE id = ?", user_id)
    # if doesn't exist, return
    if not user:
        return None
    # format and return user
    user = User(id_=user[0], name=user[1], email=user[2], profile_pic=user[3])
    return user


