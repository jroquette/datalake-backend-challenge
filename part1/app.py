"""Rest API"""

from flask import Flask, jsonify, request
from datetime import datetime

from database import products
from product import Product_Struct

app = Flask(__name__)

@app.route('/')
def home():
    """Show home message"""
    return "Bem vindo", 200


@app.route("/save_products", methods=["POST"])
def save_product():
    """
    Create a product
    :return: product
    """
    data = request.get_json()
    new_product = Product_Struct(data['id'], data['name'])
    old_product = get_product(new_product.product)
    if old_product is None:
        if not check_exists_id(new_product.product):
            products.append(new_product.product)
            return jsonify(new_product.product), 200
        return jsonify({"error": "id already exists"}), 404
    else:
        if check_product_time(old_product['created_at'], new_product.product['created_at']):
            update_value(new_product.product)
            return jsonify(new_product.product), 200
    return jsonify({"error": "not found"}), 404


@app.route("/products")
def show_products():
    """Show products """
    return jsonify(products), 200


def get_product(new_product):
    """
    Check if product exists in database
    :param new_product: product
    :return: if exists return Product else return None
    """
    for product in products:
        if new_product['hash'] == product['hash']:
            return product
    return None


def check_product_time(old_time, time_created):
    """
    check that the new time is more than 10 minutes from the old time
    :param old_time: old product time
    :param time_created: new product time
    :return: true if the time created is greater than 10 minutes from the old time
    """
    old_time = datetime.strptime(old_time, "%d/%m/%Y %H:%M:%S")
    time_created = datetime.strptime(time_created, "%d/%m/%Y %H:%M:%S")
    return ((time_created - old_time).total_seconds() / 60) >= 10


def update_value(new_product):
    """
    Update value of json
    :param new_product:
    :return:
    """
    for index in range(0, len(products)):
        old_product = products[index]
        if new_product['hash'] == old_product['hash']:
            products[index] = new_product


def check_exists_id(new_product):
    for product in products:
        if new_product['id'] == product['id']:
            return True
    return False


if __name__ == "__main__":
    app.run(debug=True)
