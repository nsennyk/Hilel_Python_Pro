import sqlite3


def get_db():
    return sqlite3.connect('db.sqlite')


def create_table():
    db = get_db()
    # Create products table with columns id, name, price
    db.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL)')


def get_products():
    db = get_db()
    # Get all products
    cursor = db.execute('SELECT * FROM products')
    return cursor.fetchall()


def create_product(name, price):
    # Create product and return prudct id
    db = get_db()
    cursor = db.execute('INSERT INTO products (name, price) VALUES (?, ?)', (name, price))
    db.commit()
    return cursor.lastrowid


def update_product(product_id, name, price):
    # Update product
    db = get_db()
    db.execute('UPDATE products SET name = ?, price = ? WHERE id = ?', (name, price, product_id))
    db.commit()


def delete_product(product_id):
    # Delete product
    db = get_db()
    db.execute('DELETE FROM products WHERE id = ?', (product_id,))
    db.commit()


if __name__ == '__main__':
    create_table()
