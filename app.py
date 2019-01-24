from flask import Flask, render_template, url_for, redirect, send_file, jsonify, abort, request, json, Response
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
db = MyDb(config.db_uri)

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
                reservation.pickup_by = db.driver(content['pickup_driver_id']) if 'pickup_driver_id' in content else reservation.pickup_by
                reservation.return_by = db.driver(content['return_driver_id']) if 'return_driver_id' in content else reservation.return_by
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
@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')

@app.route('/drivers', methods=['GET'])
def drivers():
    return render_template('drivers.html')

@app.route('/customers', methods=['GET'])
def customers():
    return render_template('customers.html')

@app.route('/reservations/<date>', methods=['GET'])
def date(date):
    return render_template('date.html', date= date)

@app.route('/users', methods=['GET'])
def users():
    return render_template('users.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')


# --- TODO ---
# Add Basic Auth
# Add permission levels (admin and user) 
#   https://stackoverflow.com/questions/15871391/implementing-flask-login-with-multiple-user-classes
#   http://blog.tecladocode.com/learn-python-defining-user-access-roles-in-flask/
#   https://realpython.com/using-flask-login-for-user-management-with-flask/
# Method for getting querystring parameter
# Add port as an input parameter
# Add HTTPS
# template pattern???
# pagination on /api/reservations and /api/cars?
# make sure that reservation with id is child or car with id
