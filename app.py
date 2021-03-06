from flask import Flask, render_template, url_for, redirect, send_file, jsonify, abort, request, json, Response, flash, session
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from functools import wraps
from model.customer import Customer
from model.car import Car
from model.reservation import Reservation
from model.driver import Driver
from model.user import User
from com.jsoncoder import Encoder
from com.http_status_code import HTTPStatusCode as http
from com.answer import Send as send
from db.orm import MyDb
import config
from flask_app import FlaskApp

app = FlaskApp(__name__)
app.secret_key = 'XkLU0VP5fmj8XTqQTHiORJ63zZcoJl'
login = LoginManager(app)
login.login_view = 'login'
db = MyDb(config.db_uri)

@login.user_loader
def load_user(id):
    user = db.user(int(id))
    session['username'] = user.name
    session['email'] = user.email
    return user

def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs): 
            with db:
                user = db.user_by_username(session['username'])
                if not user.authorize(access_level):
                    return "You do not have access to that page. Sorry!", http.NOT_AUTHORIZED
                return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/api', methods=['GET'])
def api_root():
    response = []
    for rule in app.url_map.iter_rules():
        methods = list(filter(lambda x: x in ['GET', 'POST', 'PATCH', 'DELETE', 'PUT'], rule.methods))
        response.append({'link': str(rule), 'method': ', '.join(methods)})
    return jsonify(response)

@app.route('/api/customers', methods=['GET', 'POST'])
def api_customers():
    if request.method == 'GET':
        with db:
            customers = db.customers()
            return send.ok(customers)
    elif request.method == 'POST':
        content = request.get_json()
        if Customer.valid_create(content):
            customer = Customer.create(content)
            with db:
                db.add(customer)
                return send.created(customer)
        else:
            return abort(http.BAD_REQUEST)
    else:
        return abort(http.FORBIDDEN)


@app.route('/api/customers/<customer_id>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
def api_customer(customer_id):
    customer = None
    with db:
        customer = db.customer(customer_id)
        if not customer:
            return abort(http.NOT_FOUND)
    if request.method == 'GET':
        customer = None
        with db:
            customer = db.customer(customer_id)
            return send.ok(customer)
    elif request.method == 'DELETE':
        with db:
            customer = db.customer(customer_id)
            db.delete(customer)
            return send.deleted()
    elif request.method == 'PUT':
        content = request.get_json()
        if Customer.valid_create(content):
            with db:
                customer = db.customer(customer_id)
                customer.update(content)
                return send.ok(customer)
        else:
            return abort(http.BAD_REQUEST)
    elif request.method == 'PATCH':
        content = request.get_json()
        if Customer.valid_update(content):
            with db:
                customer = db.customer(customer_id)
                customer.update(content)
                return send.patched()
        else:
            return abort(http.BAD_REQUEST)
    else:
        return abort(http.FORBIDDEN)

@app.route('/api/customers/<int:customer_id>/cars', methods=['GET', 'POST'])
def api_customer_cars(customer_id):
    if request.method == 'GET':
        with db:
            customer = db.customer(customer_id)
            return send.ok(customer.cars)
    elif request.method == 'POST':
        content = request.get_json()
        if Car.valid_create(content):
            car = Car.create(content)
            with db:
                customer = db.customer(customer_id)
                db.add(car)
                customer.cars.append(car)
                return send.created(car)
        else:
            return abort(http.BAD_REQUEST)
    else:
        return abort(http.FORBIDDEN)

@app.route('/api/customers/<int:customer_id>/cars/<int:car_id>', methods=['GET', 'PATCH'])
def api_customer_car(customer_id, car_id):
    if request.method == 'GET':
        with db:
            car = db.car(customer_id, car_id)
            if car is None:
                return '', http.NOT_FOUND
            return send.ok(car)
    elif request.method == 'PATCH':
        content = request.get_json()
        if Car.valid_update(content):
            with db:
                car = db.car(customer_id, car_id)
                car.update(content)
                return send.patched()
    else:
        return abort(http.FORBIDDEN)

@app.route('/api/customers/<int:customer_id>/cars/<int:car_id>/reservations', methods=['GET', 'POST'])
def api_customer_car_reservations(customer_id, car_id):
    if request.method == 'GET':
        with db:
            car = db.car(customer_id, car_id)
            if car is None:
                return '', http.NOT_FOUND
            return send.ok(car.reservations)
    elif request.method == 'POST':
        content = request.get_json()
        if Reservation.valid_create(content):
            reservation = Reservation.create(content)
            with db:
                car = db.car(customer_id, car_id)
                car.reservations.append(reservation)
                return send.created(reservation)
    else:
        return abort(http.FORBIDDEN)

@app.route('/api/customers/<int:customer_id>/cars/<int:car_id>/reservations/<int:reservation_id>', methods=['GET', 'DELETE', 'PATCH'])
def api_customer_car_reservation(customer_id, car_id, reservation_id):
    if request.method == 'GET':
        with db:
            reservation = db.reservation(reservation_id)
            if reservation is None:
                return '', http.NOT_FOUND
            return send.ok(reservation)
    elif request.method == 'PATCH':
        content = request.get_json()
        if Reservation.valid_update(content):
            with db:
                reservation = db.reservation(reservation_id)
                if reservation is None:
                    return '', http.NOT_FOUND
                reservation.update(content)
                #reservation.pickup_by = db.driver(content['pickup_driver_id']) if 'pickup_driver_id' in content else reservation.pickup_by
                #reservation.return_by = db.driver(content['return_driver_id']) if 'return_driver_id' in content else reservation.return_by
                print('Pickup:', reservation.pickup_driver_id, reservation.pickup_by)
                return send.patched()
        else:
            return abort(http.BAD_REQUEST)
    elif request.method == 'DELETE':
        with db:
            reservation = db.reservation(reservation_id)
            db.delete(reservation)
            return send.deleted()
    else:
        return abort(http.FORBIDDEN)


@app.route('/api/reservations', methods=['GET'])
def api_reservations():
    if request.method == 'GET':
        
        print(any(['date' in x for x in request.args]))
        ### TODO ###
        date = request.args.get('date')
        customer_id = request.args.get('customer_id', type=int)
        with db:
            reservations = db.reservations()
            if date:
                reservations = list(filter(lambda x: x.date == date, reservations))
            if customer_id:
                reservations = list(filter(lambda x: x.customer_id == customer_id, reservations))
            return send.ok(reservations)
    else:
        return abort(http.FORBIDDEN)


@app.route('/api/cars', methods=['GET'])
def api_cars():
    if request.method == 'GET':
        customer_id = request.args.get('customer_id', type=int)
        with db:
            cars = db.cars()
            if customer_id:
                cars = list(filter(lambda x: x.customer_id == customer_id, cars))
            return send.ok(cars)
    return abort(http.FORBIDDEN)


@app.route('/api/drivers', methods=['GET', 'POST'])
def api_drivers():
    if request.method == 'GET':
        with db:
            drivers = db.drivers()
            return send.ok(drivers)
    elif request.method == 'POST':
        content = request.get_json()
        if not Driver.valid_create(content):
            return abort(http.BAD_REQUEST)
        driver = Driver.create(content)
        with db:
            db.add(driver)
            return send.created(driver)    
    else:
        return abort(http.FORBIDDEN)

@app.route('/api/drivers/<int:driver_id>', methods=['GET', 'DELETE', 'PATCH'])
def api_driver(driver_id):
    if request.method == 'GET':
        driver = None
        with db:
            driver = db.driver(driver_id)
            return send.ok(driver)
    elif request.method == 'DELETE':
        with db:
            driver = db.driver(driver_id)
            db.delete(driver)
            return send.deleted()
    elif request.method == 'PATCH':
        content = request.get_json()
        if not Driver.valid_update(content):
            return abort(http.BAD_REQUEST)
        with db:
            driver = db.driver(driver_id)
            driver.update(content)
            return send.patched()
    else:
        return abort(http.FORBIDDEN)

@app.route('/api/users', methods=['GET', 'POST'])
def api_users():
    if request.method == 'GET':
        with db:
            users = db.users()
            return send.ok(users)
    elif request.method == 'POST':
        content = request.get_json()
        if not User.valid_create(content):
            return abort(http.BAD_REQUEST)
        user = User.create(content)
        with db:
            db.add(user)
            return send.created(user)    
    else:
        return abort(http.FORBIDDEN)

@app.route('/api/users/<int:user_id>', methods=['GET', 'DELETE', 'PATCH'])
def api_user(user_id):
    if request.method == 'GET':
        user = None
        with db:
            user = db.user(user_id)
            return send.ok(user)
    elif request.method == 'DELETE':
        with db:
            user = db.user(user_id)
            db.delete(user)
            return send.deleted()
    elif request.method == 'PATCH':
        content = request.get_json()
        if not User.valid_update(content):
            return abort(http.BAD_REQUEST)
        with db:
            user = db.user(user_id)
            user.update(content)
            return send.patched()
    else:
        return abort(http.FORBIDDEN)


# HTML client
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('login'))
        next = '?next={}'.format(request.args.get('next')) if 'next' in request.args else ''
        return render_template('login.html', next=next)
    if request.method == 'POST' and all(x in request.form for x in ['username', 'password']):
        username = request.form['username']
        password = request.form['password']
        with db:
            user = db.user_by_username(username)
            if user is None or not user.authenticate(password):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user)
            next_page = request.args.get('next')
            if not next_page:
                next_page = url_for('root')
            return redirect(next_page)
        return redirect(url_for('login'))

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('root'))

@app.route('/', methods=['GET'])
@login_required
def root():
    return render_template('index.html')

@app.route('/drivers', methods=['GET'])
@login_required
@requires_access_level(1)
def drivers():
    return render_template('drivers.html')

@app.route('/customers', methods=['GET'])
@login_required
@requires_access_level(1)
def customers():
    return render_template('customers.html')

@app.route('/reservations', methods=['GET'])
@login_required
@requires_access_level(1)
def date(date):
    
    return render_template('date.html', date= date)

@app.route('/reservations/<date>', methods=['GET'])
@login_required
@requires_access_level(1)
def date(date):
    return render_template('date.html', date= date)

@app.route('/users', methods=['GET'])
@login_required
@requires_access_level(2)
def users():
    return render_template('users.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')


# --- TODO ---
# Method for getting querystring parameter
# Add port as an input parameter
# Add HTTPS
# template pattern???
# pagination on /api/reservations and /api/cars?
# make sure that reservation with id is child or car with id
