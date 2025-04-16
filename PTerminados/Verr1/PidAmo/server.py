from flask import Flask, render_template, request, redirect, url_for
import logging
from datetime import datetime
import os

app = Flask(__name__)

# Configuración de logs
if not os.path.exists('logs'):
    os.makedirs('logs')
logging.basicConfig(filename='logs/app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Lista en memoria para almacenar los pedidos
orders = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/order', methods=['POST'])
def order():
    table_number = request.form.get('table_number')
    quantity_hamburguesa = int(request.form.get('quantity_hamburguesa', 0))
    quantity_cerveza = int(request.form.get('quantity_cerveza', 0))
    order_details = {
        'table': table_number,
        'items': {
            'Hamburguesa': quantity_hamburguesa,
            'Cerveza': quantity_cerveza
        },
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'Pendiente'
    }
    orders.append(order_details)
    logging.info(f"Nuevo pedido: {order_details}")
    # Se simula el procesamiento del pago y la actualización del pedido
    return redirect(url_for('order_confirmation', table=table_number))

@app.route('/order_confirmation')
def order_confirmation():
    table = request.args.get('table')
    return f"Pedido recibido para la mesa {table}. Gracias por su compra."

@app.route('/mozos')
def mozos():
    return render_template('mozos.html', orders=orders)

@app.route('/bar')
def bar():
    return render_template('bar.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
