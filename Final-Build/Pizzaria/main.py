from flask import Flask, render_template, request, session, jsonify
import sqlite3
import random
import json

app = Flask(__name__)
app.secret_key = 'hello'

queue = []
Signal = 0
count = 0
connect = sqlite3.connect('database.db')
connect.execute('DROP TABLE CLIENTS')
connect.execute('CREATE TABLE IF NOT EXISTS CLIENTS(client_first_name TEXT, client_last_name TEXT, client_phone_number TEXT, order_type TEXT, order_number INTEGER, order_status BOOL, is_placed_in_queue BOOL)')

def insert_pizza_order(order_type, order_id):
    with sqlite3.connect("database.db") as users:
        cursor = users.cursor()
        cursor.execute('INSERT INTO CLIENTS(order_type, order_number, is_placed_in_queue) VALUES(?, ?, ?)',
                           (order_type, order_id, False))

@app.route('/')
def home_page():
    return render_template('home.html', order_id=random.randint(1000, 9999))

@app.route("/order_page", methods=['POST'])
def order_page():
    if request.method == 'POST':
        order_id = request.form.get('orderId')
        session['order_id'] = order_id
        print(order_id)
        if not order_id:
            return "Error: No order ID"
        
        return render_template('index.html', order_id = order_id)
        

@app.route('/menu', methods=['POST', 'GET'])
def menu():
    if request.method == 'POST':
        order_id = request.form.get('orderId')
        session['order_id'] = order_id
        print(order_id)
        if not order_id:
            return "Error: No order ID"

        order_type = None

        if 'Pizza Margherita' in request.form:
            order_type = 'Pizza Margherita'
            insert_pizza_order(order_type, order_id)
        elif 'Pizza Pepperoni' in request.form:
            order_type = 'Pizza Pepperoni'
            insert_pizza_order(order_type, order_id)
        elif 'Pasta Carbonara' in request.form:
            order_type = 'Pasta Carbonara'
            insert_pizza_order(order_type, order_id)

        return render_template('index.html', order_type=order_type, order_id = order_id)
    else:
        return render_template('index.html')

@app.route('/shopping_cart', methods=['GET', 'POST'])
def shopping_cart():
    if request.method == 'POST':
        order_id = request.form.get('orderId')
        if order_id:
            session['order_id'] = order_id

    order_id = session.get('order_id')

    if not order_id:
        return "Error: No order ID"
    with sqlite3.connect('database.db') as connect:
        cursor = connect.cursor()
        pizza_orders = cursor.execute('SELECT order_type FROM CLIENTS WHERE order_number = ?', (order_id,)).fetchall()

    return render_template('shoppingcart.html', pizza_list = pizza_orders, len = len(pizza_orders), session_id = order_id)

@app.route('/place_order', methods=['POST'])
def place_order():

    if request.method == 'POST':
        order_id = request.form.get('session_id')
        if order_id:
            session['order_id'] = order_id

    order_id = session.get('order_id')

    print(order_id)
    if not order_id:
        return "Error: No order ID"
    
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    phone_number = request.form['phone-number']

    with sqlite3.connect('database.db') as connect:
        cursor = connect.cursor()
        cursor.execute('UPDATE CLIENTS SET client_first_name = ?, client_last_name = ?, client_phone_number = ?, order_status = ? WHERE order_number = ?',
                        (first_name, last_name, phone_number, False, order_id))
        pizza_orders = cursor.execute('SELECT order_type FROM CLIENTS WHERE order_number = ?', (order_id,)).fetchall()

    return render_template('placed_order.html', pizza_list = pizza_orders, len = len(pizza_orders))



@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    global count
    global Signal

    if request.method == 'GET':
        TestVal = Signal
        with sqlite3.connect('database.db') as connect:
            cursor = connect.cursor()

            order_number = cursor.execute('SELECT order_number FROM CLIENTS WHERE order_status = ? AND is_placed_in_queue = ?', (False, False)).fetchall()
            order_type = cursor.execute('SELECT order_type FROM CLIENTS WHERE order_status = ? AND is_placed_in_queue = ?', (False, False)).fetchall()
            first_name = cursor.execute('SELECT client_first_name FROM CLIENTS WHERE order_status = ? AND is_placed_in_queue = ?', (False, False)).fetchall()
            last_name = cursor.execute('SELECT client_last_name FROM CLIENTS WHERE order_status = ? AND is_placed_in_queue = ?', (False, False)).fetchall()
            phone_number = cursor.execute('SELECT client_phone_number FROM CLIENTS WHERE order_status = ? AND is_placed_in_queue = ?', (False, False)).fetchall()
            status = cursor.execute('SELECT order_status FROM CLIENTS').fetchall()

            for i in range(len(order_number)):
                order = {
                'Order Number': order_number[i],
                'Pizza': order_type[i],
                'Name': first_name[i],
                'Last name': last_name[i],
                'Phone number': phone_number[i],
                'Status': status[i]
            }
                queue.append(order)
                print(order)

            cursor.execute('UPDATE CLIENTS SET is_placed_in_queue = ?', (True,))
        return render_template('dashboard.html', q = queue, len = len(queue), Signal = TestVal)
    
    elif request.method == 'POST':
        data = request.get_json()
        Signal = int(data.get('SignalVal'))

        print('data received: ', Signal)
        if Signal == 1:
            queue[count]['Status'] = 1
            count = count + 1
            Signal = 0
        return jsonify({"response": "Tag Hit"})



if __name__ == "__main__":
    app.run()