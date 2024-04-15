from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import sqlite3
import hashlib
from utils import LLM

app = Flask(__name__)
app.secret_key = 'someRandomKey'

# LLM settings
MAX_LEN = 1024
CHECKPOINT_PATH = "/Users/zhuoyang/Umich/UMSI/SI-699/src/sagemaker/deberta-base-finetuned/checkpoint-2965-base1024"
# llm = LLM(CHECKPOINT_PATH, MAX_LEN)


def connect_db():
    return sqlite3.connect('var/si699.sqlite3')

def getHashedPassword(password: str):
    return "sha512$" + hashlib.sha512(password.encode()).hexdigest()

@app.route('/nav')
def nav():
    return render_template('nav.html')

# Home page route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    # Get username, email, and password from form data
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    # Hash the password
    hashed_password = getHashedPassword(password)
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
    conn.commit()
    conn.close()
    
    return redirect(url_for('login'))


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    print("login....")
    if request.method == 'POST':
        # Get username, email, and password from form data
        username = request.form['username']
        password = request.form['password']
        
        # Hash the password
        hashed_password = getHashedPassword(password)
        
        # Check credentials against the database
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        
    return render_template('login.html')


@app.route('/accounts/logout/', methods=['POST'])
def logout():
    session.pop("username", None)
    return redirect(url_for('home'))

 
@app.route("/pricing")
def pricing():
    return render_template('pricing.html')

@app.route("/products")
def products():
    return render_template('products.html')


@app.route("/api/check_text_test", methods=['POST'])
def check_text_test():
    text = request.get_json()['text']
    print("In api: " + text)
    import numpy as np
    isAI = np.random.randint(2)
    return jsonify({'isAI': isAI})


@app.route("/api/check_text", methods=['POST'])
def check_text():
    text = request.get_json()['text']
    isAI: int = llm.predict(text)
    print(isAI)
    return jsonify({'isAI': isAI})
    
   
   
@app.route("/users/<uname>", methods=["GET"])
def user_profile(uname):
    if "username" in session:
        # Check credentials against the database
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (uname,))
        user = c.fetchone()
        conn.close()
        
        ctx = {
            "user_info": {"username": user[0], "email": user[1]},
            "logname": session['username'],
        }
        return render_template("user.html", **ctx)
    
    return redirect(url_for('login'))
        
   
     
if __name__ == '__main__':
    app.run(debug=True, port=5001)