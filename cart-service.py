from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)


cart = {}

PRODUCT_SERVICE_URL = os.environ.get('PRODUCT_SERVICE_URL', 'http://localhost:5000')

# /cart/{user id} (GET): Retrieve the current contents of a user’s shopping cart, including product names, quantities, and total prices.
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    current_cart = cart.get(user_id, {}) # find the cart based on user_id, if it doesn't exist then return empty {}
    total = 0
    for item in current_cart.values():
        total += item['price'] * item['quantity']
    return jsonify({"cart": list(current_cart.values()), "total": total})


# /cart/{user id}/add/{product id} (POST): Add a specified quantity of a product to the user’s cart
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_item_to_cart(user_id, product_id):
    quantity = request.json.get('quantity', 1) # find the quantity from POST; if none specified, then only increment by 1
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    if response.status_code == 404:
        return jsonify({"Product specified does not exist"}), 404
    
    product = response.json()

    if user_id in cart:
        if product_id in cart[user_id]:
            cart[user_id][product_id]['quantity'] += quantity
        else:
            cart[user_id][product_id] = {
                "id": product_id,
                "name": product['name'],
                "price": product['price'],
                "quantity": quantity
            }

    if user_id not in cart:
        cart[user_id] = {}
        if product_id in cart[user_id]:
            cart[user_id][product_id]['quantity'] += quantity
        else:
            cart[user_id][product_id] = {
                "id": product_id,
                "name": product['name'],
                "price": product['price'],
                "quantity": quantity
            }
    
    return jsonify({"message": "Product added to cart"})


# /cart/{user id}/remove/{product id} (POST): Remove a specified quantity of a product from the user’s cart
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    quantity = request.json.get('quantity', 1)

    if user_id not in cart:
        return jsonify({"User is not in cart"}), 404
    if product_id not in cart[user_id]:
        return jsonify({"Product is not in cart"}), 404
    
    # check to see if we can safely delete from 
    if quantity >= cart[user_id][product_id]['quantity']:
        del cart[user_id][product_id]
    else:
        cart[user_id][product_id]['quantity'] -= quantity
    
    return jsonify({"Completed; removed product from cart"}), 200


@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    quantity = request.json.get('quantity', 1)

    if user_id not in cart or product_id not in cart[user_id]:
        return jsonify({"Could not find user or product"}), 404

    if cart[user_id][product_id]['quantity'] <= quantity:
        del cart[user_id][product_id]
    else:
        cart[user_id][product_id]['quantity'] -= quantity

    return jsonify({"message": "Product removed from cart"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)