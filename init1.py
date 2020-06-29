#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, Markup
import pymysql.cursors
from datetime import datetime
import random
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
    try:
        session['customer'] != None
    except KeyError:
        try:
            session['staff'] != None
        except KeyError:
            return render_template('index.html')
        else:
            return redirect(url_for('staff_home'))
    else:
        return redirect(url_for('customerHome'))
    #      session['customer'] != None:
    #     return redirect(url_for('customerHome'))
    # elif session['staff'] != None:
    #     return redirect(url_for('staff_home'))
    # else:
    #     return render_template('index.html')

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
		session['customer'] = data
		return redirect(url_for('customerHome'))
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
		session['staff'] = data
		return redirect(url_for('staff_home'))
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

@app.route('/view_flights')
def view_flights():
    return render_template('view_flights.html')

@app.route('/viewFlightsAction',  methods=['GET', 'POST'])
def viewFlightsAction():
    cursor = conn.cursor();
    try:
        user_name = session['staff']['user_name']
    except KeyError:
        return redirect(url_for('action_unauthorized'))
    query = '''SELECT airline FROM airline_staff WHERE user_name = %s;'''
    cursor.execute(query, (user_name))
    airline = cursor.fetchone()
    cursor.close()
    if airline == None:
        return redirect(url_for('action_unauthorized'))
    airline = airline['airline']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    dep_city = request.form['dept_city']
    dest_city = request.form['dest_city']
    cursor = conn.cursor();
    query = '''SELECT flight.flight_no as flight_no,
     flight.dep_datetime as dep_datetime,
     arr_datetime, base_price, seat_sold, dep_airport, arr_airport
     FROM flight
     INNER JOIN airport a1 on flight.dep_airport = a1.name
     INNER JOIN airport a2 on flight.arr_airport = a2.name
     WHERE (airline = %s)
     AND (dep_datetime >= %s)
     AND (dep_datetime <= %s)
     AND (dep_airport = %s OR a1.city = %s)
     AND (arr_airport = %s OR a2.city = %s)'''
    if start_date == '':
        start_date = 'dep_datetime'
    if end_date == '':
        end_date = 'dep_datetime'
    if dep_city == '':
        dep_city = 'dep_airport'
    if dest_city == '':
        dest_city = 'arr_airport'
    print(query)
    cursor.execute(query, (airline, start_date, end_date, dep_city, dep_city, dest_city, dest_city))
    message = cursor.fetchall()
    cursor.close()
    print(message)
    if message:
        return render_template('view_flights.html', message = message)
    else:
        return render_template('view_flights.html', error = 'no flights found based on your conditions!')

@app.route('/view_pass')
def view_pass():
    return render_template('view_pass.html')

@app.route('/viewPassAction',  methods=['GET', 'POST'])
def viewPassAction():
    cursor = conn.cursor();
    try:
        user_name = session['staff']['user_name']
    except KeyError:
        return redirect(url_for('action_unauthorized'))
    query = '''SELECT airline FROM airline_staff WHERE user_name = %s;'''
    cursor.execute(query, (user_name))
    airline = cursor.fetchone()
    cursor.close()
    if airline == None:
        return redirect(url_for('action_unauthorized'))
    airline = airline['airline']
    dept_city = request.form['dept_city']
    flight_no = request.form['flight_no']
    dept_date = request.form['dept_date']
    cursor = conn.cursor();
    query = '''SELECT take.email as email, customer.name as name
     FROM flight
     INNER JOIN airport a1 on flight.dep_airport = a1.name
     NATURAL JOIN take
     INNER JOIN customer on customer.email = take.email
     WHERE (airline = %s)
     AND (DATE(dep_datetime) = %s)
     AND (flight.flight_no = %s)
     AND (dep_airport = %s OR a1.city = %s)'''
    cursor.execute(query, (airline, dept_date, flight_no, dept_city, dept_city))
    message = cursor.fetchall()
    cursor.close()
    print(message)
    if message:
        return render_template('view_pass.html',message = message)
    else:
        return render_template('view_pass.html',error = 'no passenger found on said flight')

@app.route('/create_flight')
def create_flight():
    cursor = conn.cursor();
    try:
        user_name = session['staff']['user_name']
    except KeyError:
        return redirect(url_for('action_unauthorized'))
    query = '''SELECT airline FROM airline_staff WHERE user_name = %s;'''
    cursor.execute(query, (user_name))
    airline = cursor.fetchone()
    cursor.close()
    if airline == None:
        return redirect(url_for('action_unauthorized'))
    airline = airline['airline']
    cursor = conn.cursor();
    query = '''SELECT * FROM flight
    WHERE (airline = %s)
    AND (dep_datetime BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 30 DAY));'''
    cursor.execute(query, (airline))
    message = cursor.fetchall()
    cursor.close()
    return render_template('create_flight.html', message = message)
@app.route('/createFlightAction', methods=['POST'])
def createFlightAction():
    cursor = conn.cursor();
    try:
        user_name = session['staff']['user_name']
    except KeyError:
        return redirect(url_for('action_unauthorized'))
    query = '''SELECT airline FROM airline_staff WHERE user_name = %s;'''
    cursor.execute(query, (user_name))
    airline = cursor.fetchone()
    cursor.close()
    if airline == None:
        return redirect(url_for('action_unauthorized'))
    airline = airline['airline']
    flight_no = request.form['flight_no']
    dep_datetime = request.form['dep_datetime']
    arr_datetime = request.form['arr_datetime']
    status = request.form['status']
    base_price = request.form['base_price']
    seat_sold = request.form['seat_sold']
    dept_airport = request.form['dept_airport']
    arr_airport = request.form['arr_airport']
    airplane_id = request.form['airplane_id']
    cursor = conn.cursor();
    query = '''INSERT INTO `flight` (`flight_no`, `airline`, `dep_datetime`,
    `arr_datetime`, `status`, `base_price`, `seat_sold`, `dep_airport`, `arr_airport`, `airplane_id`)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
    try:
        cursor.execute(query, (flight_no, airline, dep_datetime, arr_datetime,
        status, base_price, seat_sold, dept_airport, arr_airport, airplane_id))
        conn.commit()
    except pymysql.Error:
        render_template('create_flight.html', error = 'flight already exists!')
    cursor.close()
    return redirect(url_for('create_flight'))

@app.route('/change_status')
def change_status():
    return render_template('change_status.html')

@app.route('/changeStatusAction', methods=['POST'])
def changeStatusAction():
    cursor = conn.cursor();
    try:
        user_name = session['staff']['user_name']
    except KeyError:
        return redirect(url_for('action_unauthorized'))
    query = '''SELECT airline FROM airline_staff WHERE user_name = %s;'''
    cursor.execute(query, (user_name))
    airline = cursor.fetchone()
    cursor.close()
    if airline == None:
        return redirect(url_for('action_unauthorized'))
    airline = airline['airline']
    flight_no = request.form['flight_no']
    dep_date = request.form['dept_date']
    dept_airport = request.form['dept_airport']
    status = request.form['status']
    cursor = conn.cursor();
    query = '''UPDATE flight
    SET status = %s
    WHERE (airline = %s) AND (flight_no = %s) AND (DATE(dep_datetime) = %s) AND (dep_airport = %s)'''
    try:
        cursor.execute(query, (status, airline, flight_no, dep_date, dept_airport))
        conn.commit()
    except pymysql.Error:
        render_template('change_status.html', error = 'Flight Not Found!')
    cursor.close()
    return render_template('change_status.html', error = 'Status Changed!')

@app.route('/add_airplane')
def add_airplane():
    cursor = conn.cursor();
    try:
        user_name = session['staff']['user_name']
    except KeyError:
        return redirect(url_for('action_unauthorized'))
    query = '''SELECT airline FROM airline_staff WHERE user_name = %s;'''
    cursor.execute(query, (user_name))
    airline = cursor.fetchone()
    cursor.close()
    if airline == None:
        return redirect(url_for('action_unauthorized'))
    airline = airline['airline']
    cursor = conn.cursor();
    query = '''SELECT * FROM airplane
    WHERE (airline = %s);'''
    cursor.execute(query, (airline))
    message = cursor.fetchall()
    cursor.close()
    return render_template('add_airplane.html', message = message)
@app.route('/addAirplane', methods=['POST'])
def addAirplane():
    cursor = conn.cursor();
    try:
        user_name = session['staff']['user_name']
    except KeyError:
        return redirect(url_for('action_unauthorized'))
    query = '''SELECT airline FROM airline_staff WHERE user_name = %s;'''
    cursor.execute(query, (user_name))
    airline = cursor.fetchone()
    cursor.close()
    if airline == None:
        return redirect(url_for('action_unauthorized'))
    airline = airline['airline']
    airplane_id = request.form['airplane_id']
    capacity = request.form['capacity']
    cursor = conn.cursor();
    query = '''INSERT INTO `airplane` (`airplane_id`, `airline`, `capacity`)
    VALUES (%s, %s, %s);'''
    try:
        cursor.execute(query, (airplane_id, airline, capacity))
        conn.commit()
    except pymysql.IntegrityError:
        return render_template('add_airplane.html', error = 'plane ID already exists!')
    cursor.close()
    return redirect(url_for('add_airplane'))

@app.route('/add_airport')
def add_airport():
    cursor = conn.cursor();
    try:
        user_name = session['staff']['user_name']
    except KeyError:
        return redirect(url_for('action_unauthorized'))
    query = '''SELECT airline FROM airline_staff WHERE user_name = %s;'''
    cursor.execute(query, (user_name))
    airline = cursor.fetchone()
    cursor.close()
    if airline == None:
        return redirect(url_for('action_unauthorized'))
    airline = airline['airline']
    cursor = conn.cursor();
    query = '''SELECT * FROM airport;'''
    cursor.execute(query)
    message = cursor.fetchall()
    cursor.close()
    return render_template('add_airport.html', message = message)
@app.route('/addAirport', methods=['POST'])
def addAirport():
    cursor = conn.cursor();
    try:
        user_name = session['staff']['user_name']
    except KeyError:
        return redirect(url_for('action_unauthorized'))
    query = '''SELECT airline FROM airline_staff WHERE user_name = %s;'''
    cursor.execute(query, (user_name))
    airline = cursor.fetchone()
    cursor.close()
    if airline == None:
        return redirect(url_for('action_unauthorized'))
    airline = airline['airline']
    name = request.form['name']
    city = request.form['city']
    cursor = conn.cursor();
    query = '''INSERT INTO `airport` (`name`, `city`)
    VALUES (%s, %s);'''
    try:
        cursor.execute(query, (name, city))
        conn.commit()
    except pymysql.IntegrityError:
        return render_template('add_airport.html', error = 'Airport already exists!')
    cursor.close()
    return redirect(url_for('add_airport'))

@app.route('/view_rating')
def view_rating():
    cursor = conn.cursor();
    try:
        user_name = session['staff']['user_name']
    except KeyError:
        return redirect(url_for('action_unauthorized'))
    query = '''SELECT airline FROM airline_staff WHERE user_name = %s;'''
    cursor.execute(query, (user_name))
    airline = cursor.fetchone()
    cursor.close()
    if airline == None:
        return redirect(url_for('action_unauthorized'))
    airline = airline['airline']
    cursor = conn.cursor();
    query = '''SELECT flight.flight_no, flight.dep_datetime, AVG(rate) as rating
    FROM flight NATURAL JOIN take
    WHERE airline = %s
    GROUP BY flight.flight_no, flight.dep_datetime;'''
    cursor.execute(query, (airline))
    message = cursor.fetchall()
    cursor.close()
    if message:
        return render_template('view_rating.html', data = message)
    else:
        return render_template('view_rating.html', error = 'flight does not exist or comment does not exist')
@app.route('/viewFlightRating', methods=['POST'])
def viewFlightRating():
    cursor = conn.cursor();
    try:
        user_name = session['staff']['user_name']
    except KeyError:
        return redirect(url_for('action_unauthorized'))
    query = '''SELECT airline FROM airline_staff WHERE user_name = %s;'''
    cursor.execute(query, (user_name))
    airline = cursor.fetchone()
    cursor.close()
    if airline == None:
        return redirect(url_for('action_unauthorized'))
    airline = airline['airline']
    flight_no = request.form['flight_no']
    dept_date = request.form['dept_date']
    cursor = conn.cursor();
    query = '''SELECT name, rate, comment
    FROM take NATURAL JOIN customer
    WHERE airline = %s AND (flight_no = %s) AND (DATE(dep_datetime) = %s);'''
    cursor.execute(query, (airline, flight_no, dept_date))
    message = cursor.fetchall()
    cursor.close()
    return render_template('view_rating.html', message = message)

@app.route('/view_frequent_cust')
def view_frequent_cust():
    cursor = conn.cursor();
    try:
        user_name = session['staff']['user_name']
    except KeyError:
        return redirect(url_for('action_unauthorized'))
    query = '''SELECT airline FROM airline_staff WHERE user_name = %s;'''
    cursor.execute(query, (user_name))
    airline = cursor.fetchone()
    cursor.close()
    if airline == None:
        return redirect(url_for('action_unauthorized'))
    airline = airline['airline']
    cursor = conn.cursor();
    query = '''SELECT take.email AS email, name, COUNT(*) AS flight_count
    FROM take NATURAL JOIN customer
    WHERE airline = %s AND YEAR(dep_datetime) = YEAR(CURDATE())
    GROUP BY email
    ORDER BY COUNT(*) DESC
    LIMIT 1;'''
    cursor.execute(query, (airline))
    data = cursor.fetchone()
    cursor.close()
    print(data)
    if data:
        return render_template('view_frequent_cust.html', data = data)
    else:
        return render_template('view_frequent_cust.html', error = 'no flights were taken this year')

@app.route('/view_cust_flights')
def view_cust_flights():
    return render_template('view_cust_flights.html')

@app.route('/viewCustFlightsAction', methods=['POST'])
def viewCustFlightsAction():
    email = request.form['email']
    cursor = conn.cursor();
    try:
        user_name = session['staff']['user_name']
    except KeyError:
        return redirect(url_for('action_unauthorized'))
    query = '''SELECT airline FROM airline_staff WHERE user_name = %s;'''
    cursor.execute(query, (user_name))
    airline = cursor.fetchone()
    cursor.close()
    if airline == None:
        return redirect(url_for('action_unauthorized'))
    airline = airline['airline']
    cursor = conn.cursor();
    query = '''SELECT dep_airport, arr_airport, flight.dep_datetime as dep_datetime, flight.flight_no as flight_no, ticket_id
    FROM take NATURAL JOIN customer NATURAL JOIN flight
    WHERE (airline = %s) AND (YEAR(dep_datetime) = YEAR(CURDATE()) - 1) AND (customer.email = %s);'''
    cursor.execute(query, (airline, email))
    data = cursor.fetchall()
    cursor.close()
    print(data)
    if data:
        return render_template('view_cust_flights.html', data = data)
    else:
        return render_template('view_cust_flights.html', error = 'no flights were taken')

@app.route('/view_sales')
def view_sales():
    return render_template('view_sales.html')

@app.route('/viewSalesAction', methods=['POST'])
def viewSalesAction():
    cursor = conn.cursor();
    try:
        user_name = session['staff']['user_name']
    except KeyError:
        return redirect(url_for('action_unauthorized'))
    query = '''SELECT airline FROM airline_staff WHERE user_name = %s;'''
    cursor.execute(query, (user_name))
    airline = cursor.fetchone()
    cursor.close()
    if airline == None:
        return redirect(url_for('action_unauthorized'))
    airline = airline['airline']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    cursor = conn.cursor();
    query = '''SELECT YEAR(sold_datetime) AS year, MONTH(sold_datetime) AS month, COUNT(*) as sales
    FROM ticket NATURAL JOIN take
    WHERE (sold_datetime BETWEEN %s AND %s) AND (airline = %s)
    GROUP BY YEAR(sold_datetime), MONTH(sold_datetime);'''
    cursor.execute(query, (start_date, end_date, airline))
    data = cursor.fetchall()
    cursor.close()
    print(data)
    labels = []
    values = []
    for each in data:
        labels.append(str(each['year'])+'-'+str(each['month']))
        values.append(each['sales'])
    return render_template('bar_chart.html', title='Monthly Sales', max=10, labels=labels, values=values)
# graphing courtesy of Ruan Bekker https://blog.ruanbekker.com/blog/2017/12/14/graphing-pretty-charts-with-python-flask-and-chartjs/

@app.route('/view_quarter')
def view_quarter():
    return render_template('view_quarter.html')

@app.route('/viewQuarterAction', methods=['POST'])
def viewQuarterAction():
    cursor = conn.cursor();
    try:
        user_name = session['staff']['user_name']
    except KeyError:
        return redirect(url_for('action_unauthorized'))
    query = '''SELECT airline FROM airline_staff WHERE user_name = %s;'''
    cursor.execute(query, (user_name))
    airline = cursor.fetchone()
    cursor.close()
    if airline == None:
        return redirect(url_for('action_unauthorized'))
    airline = airline['airline']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    cursor = conn.cursor();
    # query = '''SELECT YEAR(sold_datetime) AS year, QUARTER(sold_datetime) AS quarter, SUM(price) as revenue
    # FROM ticket NATURAL JOIN take
    # WHERE (sold_datetime BETWEEN %s AND %s) AND (airline = %s)
    # GROUP BY YEAR(sold_datetime), QUARTER(sold_datetime);'''
    query = '''SELECT YEAR(sold_datetime) AS year, QUARTER(sold_datetime) AS quarter, SUM(price) as revenue
    FROM ticket
    WHERE (sold_datetime BETWEEN %s AND %s)
    GROUP BY YEAR(sold_datetime), QUARTER(sold_datetime);'''
    # cursor.execute(query, (start_date, end_date, airline))
    cursor.execute(query, (start_date, end_date))
    data = cursor.fetchall()
    cursor.close()
    print(data)
    labels = []
    values = []
    colors = ["#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA"]
    for each in data:
        labels.append(str(each['year'])+ ' Q' +str(each['quarter']))
        values.append(each['revenue'])
    return render_template('pie_chart.html', title='Quarterly Sales', max=100000, set=zip(values, labels, colors))
# graphing courtesy of Ruan Bekker https://blog.ruanbekker.com/blog/2017/12/14/graphing-pretty-charts-with-python-flask-and-chartjs/

@app.route('/customerHome',methods=['POST','GET'])
def customerHome():
    email = session['customer']['email']
    name = session['customer']['name']
    cursor = conn.cursor()
    view_by = "dep_datetime"
    qfuture = 'SELECT airline, flight_no, dep_datetime, dep_airport, arr_airport, status FROM take NATURAL JOIN flight WHERE email = %s  AND dep_datetime > NOW() ORDER BY %s ASC'
    cursor.execute(qfuture, (email, view_by))
    future_flight = cursor.fetchall()
    qpast = 'SELECT airline, flight_no, dep_datetime, dep_airport, arr_airport,rate,comment FROM take NATURAL JOIN flight WHERE email = %s AND arr_datetime < NOW() ORDER BY %s DESC'
    cursor.execute(qpast,(email,view_by))
    past_flight = cursor.fetchall()
    cursor.execute('SELECT*FROM airport')
    city = cursor.fetchall()
    #add cities in flight informations
    for i in range(len(future_flight)):
        for n in city:
            if n['name']== future_flight[i]['dep_airport']:
                future_flight[i]['dep_city'] = n['city']
            if n['name']== future_flight[i]['arr_airport']:
                future_flight[i]['arr_city'] = n['city']
    for i in range(len(past_flight)):
        for n in city:
            if n['name']== past_flight[i]['dep_airport']:
                past_flight[i]['dep_city'] = n['city']
            if n['name']== past_flight[i]['arr_airport']:
                past_flight[i]['arr_city'] = n['city']
    return render_template('customer_home.html', name=name, email=email,future_flight=future_flight,past_flight=past_flight)
@app.route('/viewMyFlight',methods=['GET','POST'])
def view_my_flight():
    email = session['customer']['email']
    name = session['customer']['name']
    cursor = conn.cursor()
    view_by = request.form['view_by']
    qfuture = 'SELECT airline, flight_no, dep_datetime, dep_airport, arr_airport, status FROM take NATURAL JOIN flight WHERE email = %s  AND dep_datetime > NOW() ORDER BY %s ASC'
    cursor.execute(qfuture, (email, view_by))
    future_flight = cursor.fetchall()
    qpast = 'SELECT airline, flight_no, dep_datetime, dep_airport, arr_airport,rate,comment FROM take NATURAL JOIN flight WHERE email = %s AND arr_datetime < NOW() ORDER BY %s DESC'
    cursor.execute(qpast,(email,view_by))
    past_flight = cursor.fetchall()
    cursor.execute('SELECT*FROM airport')
    city = cursor.fetchall()
    #add cities in flight informations
    for i in range(len(future_flight)):
        for n in city:
            if n['name']== future_flight[i]['dep_airport']:
                future_flight[i]['dep_city'] = n['city']
            if n['name']== future_flight[i]['arr_airport']:
                future_flight[i]['arr_city'] = n['city']
    for i in range(len(past_flight)):
        for n in city:
            if n['name']== past_flight[i]['dep_airport']:
                past_flight[i]['dep_city'] = n['city']
            if n['name']== past_flight[i]['arr_airport']:
                past_flight[i]['arr_city'] = n['city']
    return render_template('customer_home.html', name=name, email=email,future_flight=future_flight,past_flight=past_flight)

@app.route('/addComment',methods=['GET','POST'])
def add_comment():
    cursor = conn.cursor()
    email = session['customer']['email']
    rate, comment = request.form["rate"], request.form["comment"]
    flight_info = (email,request.form["cr_airline"],request.form["cr_flight_no"],request.form["cr_dep_datetime"])
    cursor.execute("SELECT*FROM take WHERE email=%s AND airline=%s AND flight_no=%s AND dep_datetime=%s",flight_info)
    if cursor.fetchall() is not None and rate in ('1','2','3','4','5'):
        #store query information from html form in this tuple
        cr_flight = (request.form["rate"],request.form["comment"],email,request.form["cr_airline"],request.form["cr_flight_no"],request.form["cr_dep_datetime"])
        cursor.execute('UPDATE take SET rate=%s, comment=%s WHERE email=%s AND airline=%s AND flight_no=%s AND dep_datetime=%s',cr_flight)
        conn.commit()
        cursor.close()
        message = 'Comment Placed'
    else:
        message = 'Incorrect Format or Information'
    return render_template('customer_home.html', message=message)
@app.route('/staff_home',methods=['GET','POST'])
def staff_home():
    cursor=conn.cursor()
    airline = session["staff"]["airline"]
    qflight = 'SELECT * FROM flight WHERE airline=%s AND dep_datetime>NOW()'
    flight = cursor.execute(qflight,(airline))
    cursor.close()
    return render_template('staff_home.html')


@app.route('/customerSearch',methods=['GET','POST'])
def customerSearch():
    return render_template('customer_search.html')

@app.route('/customerSearchResult', methods=['GET', 'POST'])
def customerSearchResult():
    dept_city_airport = request.form['dept_city']
    dest_city_airport = request.form['dest_city']
    dept_date = request.form['dept_date']
    ret_date = request.form['ret_date']
    cursor = conn.cursor()
    if ret_date == '':
        query = '''SELECT flight_no, airline, dep_datetime, arr_datetime,
            dep_airport, arr_airport, a1.city AS dep_city, a2.city AS arr_city, base_price
            FROM flight
            INNER JOIN airport a1 on flight.dep_airport = a1.name
            INNER JOIN airport a2 on flight.arr_airport = a2.name
            WHERE (dep_airport = %s OR a1.city = %s) AND (arr_airport = %s OR a2.city = %s)
            AND DATE(dep_datetime) = %s;'''
        cursor.execute(query, (dept_city_airport, dept_city_airport, dest_city_airport, dest_city_airport, dept_date))
    else:
        query = '''SELECT flight_no, airline, dep_datetime, arr_datetime,
            dep_airport, arr_airport, a1.city AS dep_city, a2.city AS arr_city, base_price
            FROM flight
            INNER JOIN airport a1 on flight.dep_airport = a1.name
            INNER JOIN airport a2 on flight.arr_airport = a2.name
            WHERE ((dep_airport = %s OR a1.city = %s) AND (arr_airport = %s OR a2.city = %s)
            AND DATE(dep_datetime) = %s) OR ((dep_airport = %s OR a1.city = %s) AND (arr_airport = %s OR a2.city = %s)
            AND DATE(dep_datetime) = %s);'''
        cursor.execute(query, (
        dept_city_airport, dept_city_airport, dest_city_airport, dest_city_airport, dept_date, dest_city_airport,
        dest_city_airport, dept_city_airport, dept_city_airport, ret_date))
    flight = cursor.fetchall()
    cursor.close()
    if data:
        return render_template('flight_search.html', flight=flight)
    else:
        error = 'no flight available, please search again'
        return render_template('flight_search.html', error=error)

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    return render_template('purchase.html')
@app.route('/purchaseResult', methods=['GET', 'POST'])
def purchaseResult():
    cursor = conn.cursor()
    message = None
    while message==None:
        airline, flight_no, dep_datetime = request.form['airline'],request.form['flight_no'],request.form['dep_datetime']
        qflight = 'SELECT*FROM flight NATURAL JOIN airplane WHERE dep_datetime>NOW() AND airline= %s AND flight_no=%s AND dep_datetime=%s'
        cursor.execute(qflight, (airline, flight_no, dep_datetime))
        flight = cursor.fetchone()
        if flight is None:
            message = 'Flight Not Availible, Please Try Again'
            break
        base_price, seat_sold,capacity = int(flight['base_price']), int(flight['seat_sold']), int(flight['capacity'])
        if seat_sold >= capacity:
            message = 'Flight capacity is full'
            break
        elif seat_sold > 0.7*capacity:
            price = round(1.2*base_price,2)
        else:
            price = round(base_price,2)
        card_no, card_type, name, exp_date = request.form['card_no'], request.form['card_type'], request.form['name'], request.form['exp_date']
        sold_datetime = datetime.now()
        seat_sold += 1
        cursor.execute('SELECT ticket_id FROM ticket')
        new_ticket = str(random.randint(1000000000,9999999999))
        tickets = []
        for i in cursor.fetchall():
            tickets.append(i['ticket_id'])
        while new_ticket in tickets:
            new_ticket = str(random.randint(1000000000, 9999999999))
        add_ticket = 'INSERT INTO ticket values(%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(add_ticket,(new_ticket,price,sold_datetime,card_type,card_no,name,exp_date))
        add_take = 'INSERT INTO take values(%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(add_take,(session['customer']['email'],flight_no,airline,dep_datetime,0,'',new_ticket))
        add_passenger = 'UPDATE flight SET seat_sold=%s WHERE airline=%s AND flight_no=%s AND dep_datetime=%s'
        cursor.execute(add_passenger,(seat_sold,airline,flight_no,dep_datetime))
        conn.commit()
        cursor.close()
        message = 'Thank you, your total is:' + str(price)
        break
        #Create a new unique ticket id
    return render_template("purchase.html",message=message)

@app.route('/customerSpending',methods=['GET','POST'])
def customerSpendinng():
    cursor = conn.cursor()
    try:
        email = session['customer']['email']
    except:
        return render_template('index.html',message='please login to view your spending')
    query1 = "SELECT DATE_FORMAT(sold_datetime, '%Y-%m') AS month , SUM(price) AS total FROM ticket NATURAL JOIN take WHERE email = '"
    query2 = "' GROUP BY month ORDER BY month DESC;"
    query = query1 + str(email) + query2
    cursor.execute(query)
    spending = cursor.fetchall()
    return render_template('customer_spending.html',spending=spending)

@app.route('/logoutStaff')
def logoutStaff():
	session.pop('staff')
	return render_template('/logout.html', logged_out = 'Logged Out!')
@app.route('/logoutCustomer')
def logoutCustomer():
	session.pop('customer')
	return render_template('/logout.html', logged_out = 'Logged Out!')
@app.route('/action_unauthorized')
def action_unauthorized():
    return render_template('action_unauthorized.html')


app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
