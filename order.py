import sqlite3, os
import catalog

db_users_path = os.path.join(catalog.BASE_DIR, 'users.db')

users_data_list = []


def add_users_data_list(char):
    users_data_list.append(char)


def add_users_data_in_db(users_data_list, user_id):
    sqlite_connection = sqlite3.connect(db_users_path)
    cursor = sqlite_connection.cursor()
    sqlite_insert_data = """UPDATE data set
                            (user_name, user_surname, user_phone, user_address) = (?, ?, ?, ?) where user_id = ?"""
        # Преобразование данных в формат кортежа
    data_tuple = (users_data_list[0], users_data_list[1], users_data_list[2], users_data_list[3], user_id)
    cursor.execute(sqlite_insert_data, data_tuple)
    sqlite_connection.commit()
    cursor.close()
    users_data_list.clear()


def check_user_data(user_id):
    # Проверка данных о пользователе в базе данных
    conn = sqlite3.connect(db_users_path)
    conn.row_factory = lambda cursor, row: str(row[0])
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM data")
    all_user_id = cur.fetchall()
    conn.close()

    if str(user_id) in all_user_id:
        conn = sqlite3.connect(db_users_path)
        cur = conn.cursor()
        cur.execute("SELECT user_name, user_surname, user_phone, user_address FROM data where user_id=?", (user_id,))
        user_data = cur.fetchone()
        conn.close()
        return user_data


def get_user_id(user_id):
    conn = sqlite3.connect(db_users_path)
    cur = conn.cursor()
    cur.execute("INSERT INTO data (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()


def send_user_data(data, products):
    # Возврат данных, которые необходимо отправить менеджеру
    products_str = ''
    cart_sum = 0
    for i in products:
        products_str += f'{i[1]}:   {i[2]} рублей\n\n'
        cart_sum += i[2]
    user_data = f'Имя: {data[0]}\n\nФамилия: {data[1]}\n\nТелефон: {data[2]}\n\nАдрес: {data[3]}\n\n\nТовары в корзине:\n\n{products_str}\nСумма товаров: {cart_sum}'
    return user_data
