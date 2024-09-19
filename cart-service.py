from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# In-memory storage for carts
carts = {}

PRODUCT_SERVICE_URL = "http://localhost:5000"  # Update this when deploying

# /cart/{user id} (GET): Retrieve the current contents of a user’s shopping cart, including product names, quantities, and total prices.
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart = carts.get(user_id, {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return jsonify({"cart": list(cart.values()), "total": total})


# /cart/{user id}/add/{product id} (POST): Add a specified quantity of a product to the user’s cart
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    quantity = request.json.get('quantity', 1)
    
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    if response.status_code != 200:
        return jsonify({"error": "Product not found"}), 404
    
    product = response.json()
    
    if user_id not in carts:
        carts[user_id] = {}
    
    if product_id in carts[user_id]:
        carts[user_id][product_id]['quantity'] += quantity
    else:
        carts[user_id][product_id] = {
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
    
    if user_id not in carts or product_id not in carts[user_id]:
        return jsonify({"error": "Product not in cart"}), 404
    
    if carts[user_id][product_id]['quantity'] <= quantity:
        del carts[user_id][product_id]
    else:
        carts[user_id][product_id]['quantity'] -= quantity
    
    return jsonify({"message": "Product removed from cart"})

if __name__ == '__main__':
    app.run(port=5001)