import os, sqlite3
import catalog

db_products_path = os.path.join(catalog.BASE_DIR, 'products.db')
db_orders_path = os.path.join(catalog.BASE_DIR, 'orders.db')


def add_to_cart(user_id, product_id):
    sqlite_connection = sqlite3.connect(db_orders_path)
    cursor = sqlite_connection.cursor()

    sqlite_insert_data = """INSERT OR REPLACE INTO user_devices
                                  (user_id, device_id) VALUES (?, ?)"""

    data_tuple = (user_id, product_id)
    cursor.execute(sqlite_insert_data, data_tuple)
    sqlite_connection.commit()
    cursor.close()


def name_add_to_cart(device_id):
    # Описание товара, который добавлен в корзину
    conn = sqlite3.connect(db_products_path)
    cur = conn.cursor()
    cur.execute("SELECT category, name FROM devices where device_id=?", (device_id,))
    product_name = cur.fetchone()
    conn.close()
    return product_name


def show_cart(user_id):
    conn = sqlite3.connect(db_orders_path)
    cur = conn.cursor()
    cur.execute("SELECT device_id FROM user_devices where user_id=? order by device_id", (user_id,))
    device_id_list = cur.fetchall()
    conn.close()
    conn = sqlite3.connect(db_products_path)
    cur = conn.cursor()

    products = []
    for el in device_id_list:
        cur.execute("SELECT device_id, name, price FROM devices where device_id=?", el)
        prod = cur.fetchall()
        products.append(prod[0])
    conn.close()

    return products


def clear_cart(user_id):
    # Очистка корзины после отправки данных менеджеру
    conn = sqlite3.connect(db_orders_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM user_devices where user_id=?", (user_id,))
    conn.commit()
    conn.close()
