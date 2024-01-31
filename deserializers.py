from Hilel_Python_Pro.db import create_product, update_product
from exceptions import ValidationError


# Deserialization is from JSON (or other format) to Python object
def deserialize_product(product_json, product_id=None, partial=False):
    name = product_json.get('name')
    price = product_json.get('price')
    category_id = product_json.get('category')

    if name is None and not partial:
        raise ValidationError('name is required')
    if price is None and not partial:
        raise ValidationError('price is required')
    if category_id is None and not partial:
        raise ValidationError('category is required')

    if price is not None and price <= 0:
        raise ValidationError('price must be positive')

    if product_id is None:
        return create_product(name, price, category_id)
    else:
        return update_product(product_id, name, price, category_id)


def deserialize_category(category_json):
    name = category_json.get('name')
    is_adult_only = category_json.get('is_adult_only')

    if name is None:
        raise ValidationError('Category name is required')

    return {'name': name, 'is_adult_only': is_adult_only}