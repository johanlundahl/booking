from flask import Flask, render_template, url_for, redirect, send_file, jsonify, abort, request, json, Response
from model.customer import Customer
from model.car import Car
from model.reservation import Reservation
from model.driver import Driver
from com.jsoncoder import Encoder
from com.http_status_code import HTTPStatusCode as http
from com.answer import Send as send
from db.orm import MyDb
import config

app = Flask(__name__)
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
            return Response(response=Encoder().encode(customers), mimetype='application/json')
    elif request.method == 'POST':
        content = request.get_json()
        if 'name' in content:
            name = content['name']
            contact = content['contact'] if 'contact' in content else ''
            email = content['email'] if 'email' in content else ''
            phone = content['phone'] if 'phone' in content else ''

            customer = Customer(name, contact, phone, email)
            with db:
                db.add(customer)
            return Response(response=Encoder().encode(customer), status=http.CREATED, mimetype='application/json')
    else:
        return abort(http.BAD_REQUEST)

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
        return Response(response=Encoder().encode(customer), status=http.OK, mimetype='application/json')

    elif request.method == 'DELETE':
        with db:
            customer = db.customer(customer_id)
            db.delete(customer)
        return '', http.OK
    elif request.method == 'PUT':
        content = request.get_json()
        if content and all(x in content for x in ['name', 'contact', 'company', 'email', 'phone', 'address', 'postal_code', 'city']):
            with db:
                customer = db.customer(customer_id)
                customer.name = content['name']
                customer.contact = content['contact']
                customer.email = content['email']
                customer.phone = content['phone']
                customer.address = content['address']
                customer.postal_code = content['postal_code']
                customer.city = content['city']
                return Response(response=Encoder().encode(customer), status=http.OK, mimetype='application/json')
        else:
            return abort(http.BAD_REQUEST)
    elif request.method == 'PATCH':
        content = request.get_json()
        if content and any(x in content for x in ['name', 'contact', 'company', 'email', 'phone', 'address', 'postal_code', 'city']):
            with db:
                customer = db.customer(customer_id)
                customer.name = content['name'] if 'name' in content else customer.name
                customer.contact = content['contact'] if 'contact' in content else customer.contact
                customer.email = content['email'] if 'email' in content else customer.email
                customer.phone = content['phone'] if 'phone' in content else customer.phone
                customer.address = content['address'] if 'address' in content else customer.address
                customer.postal_code = content['postal_code'] if 'postal_code' in content else customer.postal_code
                customer.city = content['city'] if 'city' in content else customer.city
                return Response('', status=http.NO_CONTENT)
        else:
            return abort(http.BAD_REQUEST)
    else:
        return abort(http.FORBIDDEN)

@app.route('/api/customers/<int:customer_id>/cars', methods=['GET', 'POST'])
def api_customer_cars(customer_id):
    if request.method == 'GET':
        with db:
            customer = db.customer(customer_id)
            return Response(response=Encoder().encode(customer.cars), status=http.OK, mimetype='application/json')
    elif request.method == 'POST':
        content = request.get_json()
        if 'reg' in content:
            car = Car(content['reg'])
            with db:
                customer = db.customer(customer_id)
                db.add(car)
                customer.cars.append(car)
            return Response(response=Encoder().encode(car), status=http.CREATED, mimetype='application/json')
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
            return Response(response=Encoder().encode(car), status=http.OK, mimetype='application/json')
    elif request.method == 'PATCH':
        content = request.get_json()
        if 'reg' in content:
            with db:
                car = db.car(customer_id, car_id)
                car.reg = content['reg'] if 'reg' in content else car.reg
            return Response(response='', status=http.NO_CONTENT)
    else:
        return abort(http.FORBIDDEN)

@app.route('/api/customers/<int:customer_id>/cars/<int:car_id>/reservations', methods=['GET', 'POST'])
def api_customer_car_reservations(customer_id, car_id):
    if request.method == 'GET':
        with db:
            car = db.car(customer_id, car_id)
            if car is None:
                return '', http.NOT_FOUND
            return Response(response=Encoder().encode(car.reservations), status=http.OK, mimetype='application/json')
    elif request.method == 'POST':
        content = request.get_json()
        if "date" in content and "pickup_at" in content and "return_at" in content:
            date =  content['date']
            pickup_at = content['pickup_at']
            return_at = content['return_at']
            reservation = Reservation(date, pickup_at, return_at)
            with db:
                car = db.car(customer_id, car_id)
                print('FOUND CAR:', car)
                car.reservations.append(reservation)
            return Response(response=Encoder().encode(reservation), status=http.CREATED, mimetype='application/json')
    else:
        return abort(http.FORBIDDEN)

@app.route('/api/customers/<int:customer_id>/cars/<int:car_id>/reservations/<int:reservation_id>', methods=['GET', 'DELETE', 'PATCH'])
def api_customer_car_reservation(customer_id, car_id, reservation_id):
    if request.method == 'GET':
        with db:
            reservation = db.reservation(reservation_id)
            if reservation is None:
                return '', http.NOT_FOUND
            return Response(response=Encoder().encode(reservation), status=http.OK, mimetype='application/json')
    elif request.method == 'PATCH':
        content = request.get_json()
        if any([x in content for x in ['date', 'pickup_at', 'return_at']]):
            with db:
                reservation = db.reservation(reservation_id)
                if reservation is None:
                    return '', http.NOT_FOUND
                reservation.date = content['date'] if 'date' in content else reservation.date
                reservation.pickup_at = content['pickup_at'] if 'pickup_at' in content else reservation.pickup_at
                reservation.return_at = content['return_at'] if 'return_at' in content else reservation.return_at
            return Response(response='', status=http.NO_CONTENT)
        else:
            return abort(http.BAD_REQUEST)
    elif request.method == 'DELETE':
        with db:
            reservation = db.reservation(reservation_id)
            db.delete(reservation)
            return '', http.OK
    else:
        return abort(http.FORBIDDEN)

@app.route('/api/reservations', methods=['GET'])
def api_reservations():
    if request.method == 'GET':
        date = request.args.get('date')
        customer_id = request.args.get('customer_id', type=int)
        with db:
            reservations = db.reservations()
            if date:
                reservations = list(filter(lambda x: x.date == date, reservations))
            if customer_id:
                reservations = list(filter(lambda x: x.customer_id == customer_id, reservations))
            
            return Response(response=Encoder().encode(reservations), status=http.OK, mimetype='application/json')
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
            return Response(response=Encoder().encode(cars), mimetype='application/json')
    return abort(http.FORBIDDEN)


@app.route('/api/drivers', methods=['GET', 'POST'])
def api_drivers():
    if request.method == 'GET':
        with db:
            drivers = db.drivers()
            return send.ok(drivers)
    elif request.method == 'POST':
        content = request.get_json()
        if "name" not in content:
            return abort(http.BAD_REQUEST)
        driver = Driver(content['name'])
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
        if 'name' not in content:
            return abort(http.BAD_REQUEST)
        with db:
            driver = db.driver(driver_id)
            driver.name = content['name']
        return send.patched()
    else:
        return abort(http.FORBIDDEN)

if __name__ == '__main__':
    app.run(host='0.0.0.0')


# --- TODO ---
# template pattern???
# eget response objekt
# pagination on /api/reservations and /api/cars?
# make sure that reservation with id is child or car with id
#/api/drivers
#/api/users
