from flask import Flask, render_template, request, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'hello'

queue = []
connect = sqlite3.connect('database.db')
connect.execute('DROP TABLE CLIENTS')
connect.execute('CREATE TABLE IF NOT EXISTS CLIENTS(client_first_name TEXT, client_last_name TEXT, client_phone_number TEXT, order_type TEXT, order_number INTEGER, order_status BOOL)')

def insert_pizza_order(order_type, order_id):
    with sqlite3.connect("database.db") as users:
        cursor = users.cursor()
        cursor.execute('INSERT INTO CLIENTS(order_type, order_number) VALUES(?, ?)',
                           (order_type, order_id))


@app.route("/")
def main_page():
    return render_template('index.html', order_id=random.randint(1000, 9999))

@app.route('/menu', methods=['POST'])
def menu():
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

    return render_template('order_number.html', order_number=order_id, order_type=order_type)

@app.route('/shopping_cart', methods=['GET', 'POST'])
def shopping_cart():
    if request.method == 'POST':
        order_id = request.form.get('orderId')
        if order_id:
            session['order_id'] = order_id

    order_id = session.get('order_id')

    print(order_id)
    if not order_id:
        return "Error: No order ID"
    with sqlite3.connect('database.db') as connect:
        cursor = connect.cursor()
        pizza_orders = cursor.execute('SELECT order_type FROM CLIENTS WHERE order_number = ?', (order_id,)).fetchall()

    return render_template('shoppingcart.html', pizza_list = pizza_orders, len = len(pizza_orders))

@app.route('/place_order', methods=['POST'])
def place_order():
    order_id = session.get('order_id')
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    phone_number = request.form['phone-number']

    with sqlite3.connect('database.db') as connect:
        cursor = connect.cursor()
        cursor.execute('UPDATE CLIENTS SET client_first_name = ?, client_last_name = ?, client_phone_number = ?, order_status = ? WHERE order_number = ?',
                        (first_name, last_name, phone_number, False, order_id))

        order_number = cursor.execute('SELECT order_number FROM CLIENTS WHERE order_status = ?', (False,)).fetchall()
        order_type = cursor.execute('SELECT order_type FROM CLIENTS WHERE order_status = ?', (False,)).fetchall()

    for i in range(len(order_number)):
        order = {
            'Pizza_type': order_type[i],
            'Order_number': order_number[i]
        }
        queue.append(order)
        print(order)

    return render_template('placed_order.html', f_name = first_name, l_name = last_name, phone_n = phone_number)