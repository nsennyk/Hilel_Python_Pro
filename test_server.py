import requests


def test_product_create():
    # Create a product
    response = requests.post('http://localhost:5001/products', json={
        'name': 'Sandora',
        'price': 10,
    })

    print(response.status_code)
    print(response.json())


def test_product_update():
    # Update a product
    response = requests.put('http://localhost:5001/products/4', json={
        'name': 'Моршинська',
        'price': 10,
    })

    print(response.status_code)
    print(response.json())


def test_product_delete():
    # Delete a product
    response = requests.delete('http://localhost:5001/products/2')

    print(response.status_code)
    print(response.content)


def test_product_invalid_price():
    # Create a product
    response = requests.post('http://localhost:5001/products', json={
        'name': 'Ліщина',
        'price': -10,
    })

    print(response.status_code)
    print(response.json())


def test_product_update_invalid_price():
    # Update a product
    response = requests.put('http://localhost:5001/products/4', json={
        'name': 'Моршинська',
        'price': -10,
    })

    print(response.status_code)
    print(response.json())


def test_product_update():
    # Update a product
    response = requests.patch('http://localhost:5001/products/4', json={
        'name': 'Borjomi',
        'price': -100,
    })

    print(response.status_code)
    print(response.json())


def test_create_beer():
    # Create a product
    response = requests.post('http://localhost:5001/products', json={
        'name': 'Львівське',
        'price': 50,
        'category': 5,
    })

    print(response.status_code)
    print(response.json())


def test_create_category():
    # Create a category
    response = requests.post('http://localhost:5001/categories', json={
        'name': 'Soft Drinks',
        'is_adult_only': False
    })

    print(response.status_code)
    print(response.json())


def test_update_category():
    # Update a category
    response = requests.put('http://localhost:5001/categories/1', json={
        'name': 'Non-Alcoholic Beverages',
        'is_adult_only': False
    })

    print(response.status_code)
    print(response.json())


def test_delete_category():
    # Delete a category
    response = requests.delete('http://localhost:5001/categories/1')

    print(response.status_code)
    print(response.content)


if __name__ == "__main__":
    test_create_category()
    test_update_category()
    test_delete_category()

