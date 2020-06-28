#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import matplotlib
#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='project_1',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/public_info')
def publicInfo():
    return render_template('public_info.html')

@app.route('/flight_search')
def flightSearch():
    return render_template('flight_search.html')

@app.route('/flightStatusAction', methods = ['POST'])
def flightStatusAction():
    dept_city_airport = request.form['dept_city']
    dept_date = request.form['dept_date']
    airline = request.form['airline']
    flight_no = request.form['flight_no']
    cursor = conn.cursor()
    query = '''SELECT flight_no, airline, dep_datetime, status
    FROM flight
    INNER JOIN airport a1 on flight.dep_airport = a1.name
    INNER JOIN airport a2 on flight.arr_airport = a2.name
    WHERE (dep_airport = %s OR a1.city = %s)
    AND flight_no = %s
    AND DATE(dep_datetime) = %s
    AND airline = %s;'''
    cursor.execute(query, (dept_city_airport, dept_city_airport, flight_no, dept_date, airline))
    data = cursor.fetchone()
    cursor.close()
    if data:
        return render_template('flight_status.html', message = data)
    else:
        error = 'flight not found, please search again'
        return render_template('flight_status.html', error = error)


@app.route('/flightSearchAction', methods = ['POST'])
def flightSearchAction():
    dept_city_airport = request.form['dept_city']
    dest_city_airport = request.form['dest_city']
    dept_date = request.form['dept_date']
    ret_date = request.form['ret_date']
    cursor = conn.cursor()
    if ret_date == '':
        query = '''SELECT flight_no, airline, dep_datetime, arr_datetime,
        dep_airport, arr_airport, a1.city AS dep_city, a2.city AS arr_city
        FROM flight
        INNER JOIN airport a1 on flight.dep_airport = a1.name
        INNER JOIN airport a2 on flight.arr_airport = a2.name
        WHERE (dep_airport = %s OR a1.city = %s) AND (arr_airport = %s OR a2.city = %s)
        AND DATE(dep_datetime) = %s;'''
        cursor.execute(query, (dept_city_airport, dept_city_airport, dest_city_airport, dest_city_airport, dept_date))
    else:
        query = '''SELECT flight_no, airline, dep_datetime, arr_datetime,
        dep_airport, arr_airport, a1.city AS dep_city, a2.city AS arr_city
        FROM flight
        INNER JOIN airport a1 on flight.dep_airport = a1.name
        INNER JOIN airport a2 on flight.arr_airport = a2.name
        WHERE ((dep_airport = %s OR a1.city = %s) AND (arr_airport = %s OR a2.city = %s)
        AND DATE(dep_datetime) = %s) OR ((dep_airport = %s OR a1.city = %s) AND (arr_airport = %s OR a2.city = %s)
        AND DATE(dep_datetime) = %s);'''
        cursor.execute(query, (dept_city_airport, dept_city_airport, dest_city_airport, dest_city_airport, dept_date, dest_city_airport, dest_city_airport, dept_city_airport, dept_city_airport, ret_date))
    data = cursor.fetchall()
    cursor.close()
    if data:
        return render_template('flight_search.html', message = data)
    else:
        error = 'no flight available, please search again'
        return render_template('flight_search.html', error = error)


@app.route('/flight_status')
def flightStatus():
    return render_template('flight_status.html')
#Define route for login
@app.route('/customer_login')
def loginCustomer():
	return render_template('customer_login.html')
#Define route for login
@app.route('/staff_login')
def loginStaff():
	return render_template('staff_login.html')
#Define route for customer register
@app.route('/customer_register')
def registerCustomer():
	return render_template('customer_register.html')
#Define route for staff register
@app.route('/staff_register')
def registerStaff():
	return render_template('staff_register.html')
#Authenticates the login
@app.route('/loginAuthCustomer', methods=['GET', 'POST'])
def loginAuthCustomer():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email = %s and password = MD5(%s)'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('customer_login.html', error=error)
#Authenticates the login
@app.route('/loginAuthStaff', methods=['GET', 'POST'])
def loginAuthStaff():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airline_staff WHERE user_name = %s and password = MD5(%s)'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('staff_login.html', error=error)
#Authenticates the register for customer
@app.route('/registerAuthCustomer', methods=['GET', 'POST'])
def registerAuthCustomer():
	#grabs information from the forms
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    phone_no = request.form['phone_no']
    date_of_birth = request.form['date_of_birth']
    passport_no = request.form['passport_no']
    passport_exp = request.form['passport_exp']
    passport_country = request.form['passport_country']
    state = request.form['state']
    city = request.form['city']
    street = request.form['street']
    building_no = request.form['building_no']
	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (email))
	#stores the results in a variable
    data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
		#If the previous query returns data, then user exists
	    error = "This user already exists"
	    return render_template('customer_register.html', error = error)
    else:
	    ins = 'INSERT INTO customer VALUES(%s, MD5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
	    cursor.execute(ins, (email, password, name, phone_no, date_of_birth, passport_no, passport_exp, passport_country, state, city, street, building_no))
	    conn.commit()
	    cursor.close()
	    return render_template('index.html')
@app.route('/registerAuthStaff', methods=['GET', 'POST'])
# staff register
def registerAuthStaff():
	#grabs information from the forms
    user_name = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    airline = request.form['airline']
	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM airline_staff WHERE user_name = %s'
    cursor.execute(query, (user_name))
	#stores the results in a variable
    data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
		#If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('staff_register.html', error = error)
    else:
        ins = 'INSERT INTO airline_staff VALUES(%s, MD5(%s), %s, %s, %s, %s)'
        cursor.execute(ins, (user_name, password, first_name, last_name, date_of_birth, airline))
        conn.commit()
        cursor.close()
        return render_template('index.html')

@app.route('/home')
def home():

    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall()
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('home.html', username=username, posts=data1)

@app.route('/view_frequent_cust')
def view_frequent_cust():
    cursor = conn.cursor();
    username = session['username']
    query = '''SELECT airline FROM airline_staff WHERE user_name = %s;'''
    cursor.execute(query, (username))
    airline = cursor.fetchone()
    cursor.close()
    query = '''SELECT take.email, COUNT(*)
    FROM take NATURAL JOIN customer
    WHERE airline = %s
    GROUP BY email
    ORDER BY COUNT(*) DESC
    LIMIT 1;'''
    cursor.execute(query, (airline))
    data = cursor.fetchone()
    cursor.close()
    if data:
        return render_template('view_frequent_cust.html', data = data)
    else:
        return render_template('view_frequent_cust.html', error = 'no flights were taken')

@app.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = conn.cursor();
	blog = request.form['blog']
	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	cursor.execute(query, (blog, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
