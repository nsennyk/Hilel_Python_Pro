from flask import Flask, request, jsonify

from db import (
    get_products, create_product, update_product, delete_product,
    create_category, get_categories, update_category, delete_category, get_category
)
from exceptions import ValidationError
from serializers import serialize_product, serialize_category
from deserializers import deserialize_product, deserialize_category

app = Flask(__name__)


@app.route('/hello_world')
def hello_world():
    return "Hello, World!"


@app.route('/products', methods=['GET', 'POST'])
def products_api():
    if request.method == "GET":
        name_filter = request.args.get('name')
        products = get_products(name_filter)

        products_dicts = [serialize_product(product) for product in products]
        return jsonify(products_dicts)

    if request.method == "POST":
        product = deserialize_product(request.get_json())
        return jsonify(serialize_product(create_product(product))), 201


@app.route('/products/<int:product_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def product_api(product_id):
    if request.method == "GET":
        product = get_products(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify(serialize_product(product))

    if request.method in ["PUT", "PATCH"]:
        product = deserialize_product(request.get_json(), product_id, partial=request.method == "PATCH")
        return jsonify(serialize_product(update_product(product)))

    if request.method == "DELETE":
        delete_product(product_id)
        return "", 204


@app.route('/categories', methods=['GET', 'POST'])
def categories_api():
    if request.method == "GET":
        categories = get_categories()
        categories_dicts = [serialize_category(category) for category in categories]
        return jsonify(categories_dicts)

    if request.method == "POST":
        try:
            category = deserialize_category(request.get_json())
            create_category(category['name'], category['is_adult_only'])
            return jsonify({'message': 'Category created successfully'}), 201
        except ValidationError as e:
            return jsonify({'error': str(e)}), 422


@app.route('/categories/<int:category_id>', methods=['GET', 'PUT', 'DELETE'])
def category_api(category_id):
    category = get_category(category_id)

    if not category and request.method in ["GET", "PUT", "DELETE"]:
        return jsonify({'error': 'Category not found'}), 404

    if request.method == "GET":
        return jsonify(serialize_category(category))

    if request.method in ["PUT", "DELETE"]:
        try:
            category_data = request.get_json()
            update_category(category_id, category_data['name'], category_data['is_adult_only'])
            return jsonify({'message': 'Category updated successfully'})
        except ValidationError as e:
            return jsonify({'error': str(e)}), 422

        if request.method == "DELETE":
            delete_category(category_id)
            return jsonify({'message': 'Category deleted successfully'})


@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return {'error': str(e)}, 422


if __name__ == '__main__':
    app.run(debug=True, port=5001)