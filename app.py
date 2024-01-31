from flask import Flask, request, jsonify

from db import get_products, create_product, update_product, delete_product, create_category, get_categories, \
    update_category, delete_category
from exceptions import ValidationError
from serializers import serialize_product, serialize_category
from deserializers import deserialize_product, deserialize_category

app = Flask(__name__)


@app.route('/hello_world')
def hello_world():
    # Return hello world
    return "Hello, World!"


@app.route('/products', methods=['GET', 'POST'])
def products_api():
    if request.method == "GET":
        name_filter = request.args.get('name')

        products = get_products(name_filter)

        # Convert products to list of dicts
        products_dicts = [
            serialize_product(product)
            for product in products
        ]

        # Return products
        return products_dicts
    if request.method == "POST":
        # Create a product
        product = deserialize_product(request.get_json())

        # Return success
        return serialize_product(product), 201


@app.route('/products/<int:product_id>', methods=['PUT', 'PATCH', 'DELETE'])
def product_api(product_id):
    if request.method == "PUT":
        # Update a product
        product = deserialize_product(request.get_json(), product_id)
        # Return success
        return serialize_product(product)
    if request.method == "PATCH":
        # Update a product
        product = deserialize_product(request.get_json(), product_id, partial=True)
        # Return success
        return serialize_product(product)
    if request.method == "DELETE":
        delete_product(product_id)

        return "", 204


@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return {
        'error': str(e)
    }, 422


def categories_api():
    if request.method == "GET":
        categories = get_categories()

        # Convert categories to list of dicts
        categories_dicts = [
            serialize_category(category)
            for category in categories
        ]

        # Return categories
        return jsonify(categories_dicts)

    if request.method == "POST":
        try:
            # Create a category
            category = deserialize_category(request.get_json())
            create_category(category['name'], category['is_adult_only'])
            return jsonify({'message': 'Category created successfully'}), 201
        except ValidationError as e:
            return jsonify({'error': str(e)}), 422


@app.route('/categories/<int:category_id>', methods=['PUT', 'DELETE'])
def category_api(category_id):
    if request.method == "PUT":
        try:
            # Update a category
            category = deserialize_category(request.get_json())
            update_category(category_id, category['name'], category['is_adult_only'])
            return jsonify({'message': 'Category updated successfully'})
        except ValidationError as e:
            return jsonify({'error': str(e)}), 422

    if request.method == "DELETE":
        delete_category(category_id)
        return jsonify({'message': 'Category deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True, port=5001)

