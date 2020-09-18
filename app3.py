from flask import Flask, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
import mysql.connector as sqltor
from pymysql.cursors import DictCursor
import re
import datetime

app = Flask(__name__)

app.secret_key = 'sk'

mysql = MySQL(cursorclass=DictCursor)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Powerman2003'
app.config['MYSQL_DATABASE_DB'] = 'pythonlogin'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()
  
@app.route('/', methods=['GET', 'POST'])
def Home():
     return render_template('main.html')

@app.route('/pythonlogin', methods=['GET', 'POST'])
def login():
   msg = ''
   if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
      username = request.form['username']
      password = request.form['password']
      # Check if account exists using MySQL
      cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
      # Fetch one record and return result
      account = cursor.fetchone()
      # If account exists in accounts table in out database
      if account:
          # Create session data, we can access this data in other routes
         session['loggedin'] = True
         session['id'] = account['id']
         session['username'] = account['username']
         session['role'] = account['role']
         if session['role'] == 'admin':
                return redirect(url_for('admin'))
         # Redirect to home page
         return redirect(url_for('home'))
      else:
         # Account doesnt exist or username/password incorrect
         msg = 'Incorrect username/password!'
         # Show the login form with message (if any)
   return render_template('index.html', msg=msg)




@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, NULL)', (username, password, email,))
            conn.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty...
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/pythonlogin/home', methods=['GET', 'POST'])
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM buses')
        buslist = cursor.fetchall()
        Bid = request.args.get('id')
        if Bid:
            quotes='`'
            Bidcheck= quotes + Bid + quotes
            cursor.execute('DELETE FROM buses WHERE busid = %s', (Bid,))
            cursor.execute(""" DROP TABLE"""+ Bidcheck)
            conn.commit()
            return redirect(url_for('home'))
        else:
            pass
        if request.method == 'POST' and 'busid' in request.form and 'busroute' in  request.form:
                 busid = request.form['busid'] 
                 busroute = request.form['busroute']
                 Btype = request.form['type']
                 duration = request.form['duration']
                 seats = request.form['seats']
                 cost = request.form['cost']
                 Bdate = request.form.get("date")
                 time = request.form['time']
                 cursor.execute('INSERT INTO buses VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (busid, busroute, seats, duration, Btype, cost,Bdate, time))
                 cursor.execute(""" CREATE TABLE  `%s` (CusID int,CusName varchar(50),CusMail varchar(50),nofseats int,amt int)""" %(busid))
                 conn.commit()   
                 return redirect(url_for('home'))
        # User is loggedin show them the home page   
        return render_template('home.html', account=account ,buslist=buslist)
    # User is not loggedin redirect to login page
    return redirect(url_for('login')) 

@app.route('/pythonlogin/profile')
def profile(): 
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/pythonlogin/admin', methods=['GET', 'POST'])
def admin():
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM accounts')
        account = cursor.fetchall()
        if request.method == 'POST' and 'delID' in request.form:
                 iD = request.form['delID']
                 cursor.execute('DELETE FROM accounts WHERE id = %s', (iD,))
                 return redirect(url_for('admin'))
        # Show the profile page with account info
        return render_template('admin.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/pythonlogin/busbook', methods=['GET', 'POST'])
def book():
    # Check if user is loggedin
    if 'loggedin' in session:
        msg=''
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        passenger= ''
        if account['role'] == 'admin':
              br = request.args.get('br')
              cursor.execute(""" SELECT * FROM  `%s` """ %(br))
              passenger = cursor.fetchall()
        br = request.args.get('br')
        cursor.execute('SELECT * FROM buses  WHERE busid = %s', (br,))
        busChose = cursor.fetchone()
        totalseats= 0
        costperseat=0
        while busChose:
             totalseats += busChose['seats']
             costperseat += busChose['cost']
             busChose = cursor.fetchone()
        if request.method == 'POST' and 'psgrID' in request.form:
                 psgrID = request.form['psgrID']
                 CusName = request.form['CustName']
                 CusEmail = request.form['CusEmail']
                 nofseats = request.form['nofseats']
                 br = request.form['busID']
                 quotes='`'
                 brcheck= quotes + br + quotes
                 cursor.execute('SELECT * FROM buses  WHERE busid = %s', (br,))
                 busSelect = cursor.fetchone()
                 totalseats += busSelect['seats']
                 costperseat += busSelect['cost']
                 if totalseats!=0: 
                     x = int(nofseats)
                     totalseats-=x
                     amt = costperseat * x  
                     cursor.execute(""" INSERT INTO """ + brcheck +""" VALUES (%s, %s, %s, %s, %s);""",(psgrID, CusName, CusEmail, x, amt))
                     cursor.execute('UPDATE buses set seats = %s where busid = %s', (totalseats, br))
                     conn.commit() 
                     msg = "Seats are Booked"
                 else:
                     msg = "Bus Booked, No seats available"
        return render_template('busbook.html', account=account ,psgr=passenger , msg=msg, totalseats=totalseats, costperseat=costperseat)
     # User is not loggedin redirect to login page
    return redirect(url_for('login'))

        
    
if __name__=="__main__":
     app.run(debug=True)
 