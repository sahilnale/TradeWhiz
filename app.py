from functools import wraps
from flask import Flask, redirect, render_template, request, session, url_for, flash
from pyMongo import MongoClient


app = Flask(__name__)

app.config["SECRET_KEY"] = "erewewewrwe"
app.config["MONGODB_URI"] = " "

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrap

@app.route('/')
@login_required
def index():
    return("home.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")



hi = "him"