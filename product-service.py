from flask import Flask, jsonify, request

app = Flask(__name__)


product_list = [
    {'id': 1, 'name': 'Donuts', 'price': 5, 'quantity': 30},
    {'id': 2, 'name': 'Bananas', 'price': 0.45, 'quantity': 50},
    {'id': 3, 'name': 'Bread', 'price': 1.50, 'quantity': 100},
    {'id': 4, 'name': 'Fish', 'price': 8, 'quantity': 10},
]

product_id = len(product_list) #current product_id

# /products (GET): Retrieve a list of available grocery products, including their names, prices, and quantities in stock.
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(product_list), 200 #jsonify returns the product_list as a JSON response; return with 200 OK status code

# /products/product id (GET): Get details about a specific product by its unique ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    for p in product_list:
        if p['id'] == product_id:
            return jsonify(p), 200
    return 404


# /products (POST): Allow the addition of new grocery products to the inventory with information such as name, price, and quantity.
@app.route('/products', methods=['POST'])
def add_product():
    global product_list
    data = request.json
    added_product = {
        "id": len(product_list) + 1,
        "name": data["name"],
        "price": data["price"],
        "quantity": data["quantity"]
    }
    product_list.append(added_product)
    return jsonify(added_product), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
