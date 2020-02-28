from flask import Flask, jsonify, request
from orders import get_customer_details, get_order_details, create_customer, create_order, create_shipment

app= Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Monlith Breakdown !"

@app.route('/get_customer_details')
def get_customer_detail():
    num= request.args.get('num')
    print(num)
    all_customer = get_customer_details(num)
    return jsonify({'Customer Name': all_customer})

@app.route('/get_order_details')
def get_order_detail():
    num2=request.args.get('num2')
    print(num2)
    all_orders = get_order_details(num2)
    order_item = all_orders[0]
    order_value = all_orders[1]
    #print("All orders " + all_orders)
    return jsonify({'Order Items':order_item,
                   'Order Value':order_value})
    
@app.route('/create_customer', methods=['POST'])
def create_customers():
    customer_names = request.form.get('customer_name')
    customer_adds = request.form.get('customer_add')
    customer_phones = request.form.get('customer_phone')
    customer_id = create_customer(customer_names,customer_adds, customer_phones)
    return jsonify({'Customer Id':customer_id})

@app.route('/create_order', methods=['POST'])
def create_orders():
    customer_id = request.form.get('customer_id')
    order_items = request.form.get('order_item')
    order_value = request.form.get('order_value')
    shipper = request.form.get('shipper')
    order_id = create_order(customer_id,order_items, order_value)
    shipment_id = create_shipment(order_id, shipper)
    
    return jsonify({'Order Id':order_id,
                    'Shipment Id':shipment_id})

if __name__== '__main__':
    app.run(debug=False,host='0.0.0.0')
