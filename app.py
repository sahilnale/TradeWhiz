from functools import wraps
from flask import Flask, redirect, render_template, request, session, url_for, flash
from flask_session import Session
from pymongo import MongoClient,UpdateOne
from passlib.hash import pbkdf2_sha256
import uuid
import requests


app = Flask(__name__)

app.config["SECRET_KEY"] = "erewewewrwe"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

client = MongoClient("mongodb+srv://sahilnale:Logic!23@stocks.uelt6jz.mongodb.net/")
app.db = client.stocktrader

stock_key ='YTMVZXBN56T8IAM7'


def stock_quote(ticker):
        url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={}&apikey={}'.format(ticker, stock_key)
        response = requests.get(url)
        data = response.json()
        price = data['Global Quote']['05. price']
        return price

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route('/quote', methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        ticker = request.form.get('ticker')
        price = stock_quote(ticker)
        return render_template("quote.html", ticker=ticker,price=price)
    
    return render_template("quoted.html")

@app.route('/buy', methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        ticker = request.form.get('ticker')
        number = int(request.form.get('number'))
        price = float(stock_quote(ticker))
        stock = {"ticker":ticker,"price":price,"number":number}

        user_data = app.db.entries.find_one({"username":session["username"]})
        portfolio = user_data['portfolio']

        append = True

        if number*price > user_data['cash']:
            flash('Value exceeds cash available') 
            return redirect(url_for('buy'))

        for s in portfolio:
            if s['ticker'] == ticker:
                total_amount = float(s['price']) * float(s['number'])
                total_amount += price*number
                s['number'] = int(s['number']) + int(number)
                s['price'] = total_amount/int(s['number'])
                
                append = False

        user_data['cash'] -= price*number    
        if append:
            portfolio.append(stock)
        
        transactions = user_data['transactions']
        transactions.append('Bought '+ str(number) + ' Shares of ' + ticker + ' at $' + str(price))
        
        app.db.entries.update_one({"username":session['username']},{"$set": {"portfolio":portfolio}})
        app.db.entries.update_one({"username":session['username']},{"$set": {"cash":user_data['cash']}})
        app.db.entries.update_one({"username":session['username']},{"$set": {"transactions":transactions}})

        return redirect("/")
    return render_template("buy.html")


@app.route('/sell', methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        ticker = request.form.get('ticker')
        number = int(request.form.get('number'))
        price = float(stock_quote(ticker))
        stock = {"ticker":ticker,"price":price,"number":number}

        user_data = app.db.entries.find_one({"username":session["username"]})
        portfolio = user_data['portfolio']

        append = True

        for s in portfolio:
            if s['ticker'] == ticker:
                total_amount = float(s['price']) * float(s['number'])
                total_amount = float(total_amount)-(float(price)*int(number))
                if number > s['number']:
                    flash('Cannot sell more shares than owned')
                    return redirect(url_for('sell'))
                
                s['number'] = int(s['number']) - int(number)
                
                if int(s['number']) == 0:
                    portfolio.remove(s)
                else:
                    s['price'] = total_amount/int(s['number'])
                user_data['cash'] += price*number    
                append = False

                

        transactions = user_data['transactions']
        transactions.append('Sold '+ str(number) + ' Shares of ' + ticker + ' at $' + str(price))
        
        app.db.entries.update_one({"username":session['username']},{"$set": {"portfolio":portfolio}})
        app.db.entries.update_one({"username":session['username']},{"$set": {"cash":user_data['cash']}})
        app.db.entries.update_one({"username":session['username']},{"$set": {"transactions":transactions}})
        

        return redirect("/")
    return render_template("sell.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        print(username)
        password = request.form.get('password')

        user_data = app.db.entries.find_one({"username":username})
        print(user_data)

        if not user_data:
            return "hi"
        
        user = User()
        user._id = user_data["_id"]
        user.username = user_data["username"]
        user.password = user_data["password"]

        

        if user and pbkdf2_sha256.verify(password, user_data["password"]):
            session["user_id"] = user._id
            session["username"] = user.username
        
        return redirect("/")
        
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        print(username)
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        if not username:
            flash('Username is Required') 
            return redirect(url_for('register'))
        elif not password:
            flash('Password is Required')
            return redirect(url_for('register'))
        
        elif not confirmation:
            flash('Password is Required')
            return redirect(url_for('register'))

        if password != confirmation:
            flash('Passwords need to match')
            return redirect(url_for('register'))
        
        user = {
            "_id": uuid.uuid4().hex,
            "username":username,
            "password":password,
            "portfolio":[],
            "cash":10000,
            "transactions":[]
        }

        user['password'] = pbkdf2_sha256.encrypt(user['password'])
 
        app.db.entries.insert_one(user)
        return redirect('/')

    else:
        return render_template("register.html")
    


@app.route("/logout", methods=["GET", "POST"])

def logout():
    session.clear()
    return redirect('/')

@app.route('/',methods=["GET", "POST"])
@login_required
def index():
    user_data = app.db.entries.find_one({"username":session["username"]})
    portfolio = user_data['portfolio']
    cash = user_data['cash']
    total_value = 0
    for stock in portfolio:
        total_value += stock['price']*stock['number']
    total_value += cash
    return render_template("home.html",portfolio=portfolio,cash=cash, total_value=total_value)

@app.route('/history',methods=["GET", "POST"])
@login_required
def history():
    user_data = app.db.entries.find_one({"username":session["username"]})
    transactions = user_data['transactions']
    return render_template("history.html",transactions=transactions)


port_number = 7000

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=port_number)

class User:
    _id:str
    username:str
    password:str
    portfolio:[]
    cash:float
    transactions:[]


