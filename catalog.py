import os, sqlite3


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_products_path = os.path.join(BASE_DIR, 'products.db')
categories = ['Телефоны', 'Ноутбуки', 'Гарнитура']

products_list = []


def add_products_list(char):
    products_list.append(char)


def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        img = file.read()
    return img

# def convert_to_binary_data(filename):
#     # Преобразование данных в двоичный формат
#     img = Image.open(filename)
#     img = numpy.array(img)
#     binarr = numpy.where(img>128, 255, 0)
#     return binarr


def add_products_in_db(products_list):
    sqlite_connection = sqlite3.connect(db_products_path)
    cursor = sqlite_connection.cursor()
    sqlite_insert_blob_query = """INSERT OR REPLACE INTO devices
                                  (category, name, description, price, image) VALUES (?, ?, ?, ?, ?)"""
    image = convert_to_binary_data(products_list[4])
        # Преобразование данных в формат кортежа
    data_tuple = (products_list[0], products_list[1], products_list[2], products_list[3], image)
    cursor.execute(sqlite_insert_blob_query, data_tuple)
    sqlite_connection.commit()
    cursor.close()
    products_list.clear()


def write_image(data, filename):
    with open(filename,'wb') as file:
        file.write(data)


def get_products_list(category):
    # Возврат продуктов из базы данных, соответствующих данной категории
    conn = sqlite3.connect(db_products_path)
    cur = conn.cursor()

    cur.execute("SELECT * FROM devices where category=?", (category,))
    products = cur.fetchall()

    conn.close()
    return products


def get_products_id_lists():
    # Получение списка всех device_id
    conn = sqlite3.connect(db_products_path)
    conn.row_factory = lambda cursor, row: str(row[0])
    cur = conn.cursor()
    cur.execute("SELECT device_id FROM devices")
    products_id = cur.fetchall()
    conn.close()
    return products_id


def get_product_id_to_cart():
    device_id = get_products_id_lists()
    device_id_cart = [i+'cart' for i in device_id]
    return device_id_cart


def get_device(product_id):
    conn = sqlite3.connect(db_products_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM devices where device_id=?", (product_id,))
    device = list(cur.fetchall()[0])
    categ = device[1]
    image_data = device[5]

    picture_path = os.path.join(BASE_DIR, 'pictures', str(product_id) + "_%s.jpg" % categ)
    write_image(image_data, picture_path)
    device[5] = picture_path
    conn.close()

    return device
