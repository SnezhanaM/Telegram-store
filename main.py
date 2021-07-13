import telebot
import os
import config, catalog, cart, order
from telebot import types

bot = telebot.TeleBot(config.token)


def admin_button(message):
    button = types.ReplyKeyboardMarkup(True)
    button.row('Добавить позицию')

    return bot.send_message(message.chat.id, 'Привет, админ.\nЕсли хочешь добавить позиции, жми на кнопку.', reply_markup=button)


def main_menu():
    keyboard1 = types.InlineKeyboardMarkup(row_width=2)
    for i in range(len(catalog.categories)):
        item_cat = types.InlineKeyboardButton(catalog.categories[i], callback_data=catalog.categories[i])
        keyboard1.row(item_cat)

    return keyboard1


@bot.message_handler(commands=['start'])
def welcome(message):
    if message.chat.id == config.test_id:
        admin_button(message)

    else:
        button = types.ReplyKeyboardMarkup(True, True)
        button.row('Да, конечно!')

        bot.send_message(message.chat.id, 'Добрый день! Привествуем тебя в нашем магазине. '
                                          'Готов приступить к выбору техники?', reply_markup=button)


@bot.message_handler(content_types=['text'])
def send_menu(message):
    if message == 'back' or message.text == 'Да, конечно!':
        bot.send_message(message.chat.id, 'Отлично! Предлагаю выбрать из списка', reply_markup=main_menu())
        cart_button = types.ReplyKeyboardMarkup(True)
        cart_button.row('Корзина')
        bot.send_message(message.chat.id, 'Чтобы посмотреть Вашу корзину, нажмите на кнопку ниже', reply_markup=cart_button)

    elif message.text == 'Корзина':
        user_id = message.chat.id
        products_in_cart = cart.show_cart(user_id)

        if not products_in_cart:
            bot.send_message(message.chat.id, 'Ваша корзина пока пуста')

        else:
            products_str = ''
            cart_sum = 0
            for i in products_in_cart:
                products_str += f'{i[1]}:   {i[2]} рублей\n\n'
                cart_sum += i[2]
            bot.send_message(message.chat.id, 'Товары в Вашей корзине: \n\n%s\nСумма товаров: %s рублей' % (products_str, cart_sum))

            keyboard_ordering = types.InlineKeyboardMarkup(row_width=2)
            item_ordering = types.InlineKeyboardButton('Оформить заказ', callback_data='ordering')
            clearing_cart = types.InlineKeyboardButton('Очистить корзину', callback_data='clearing')
            keyboard_ordering.add(item_ordering, clearing_cart)
            bot.send_message(message.chat.id, 'Для оформления заказа нажмите на кнопку "Оформить заказ"',
                             reply_markup=keyboard_ordering)

    elif message.chat.id == config.test_id and message.text == 'Добавить позицию':
        catalog.products_list.clear()
        bot.send_message(message.chat.id, "Введите категорию устройства")
        bot.register_next_step_handler(message, get_category)


def user_data_output(chat_id, user_data):
    keyboard3 = types.InlineKeyboardMarkup(row_width=2)
    item_yes = types.InlineKeyboardButton('Да', callback_data='yes_order')
    item_no = types.InlineKeyboardButton('Нет', callback_data='no_order')
    keyboard3.add(item_yes, item_no)

    bot.send_message(chat_id, f"Проверьте Ваши данные \n\nИмя: {user_data[0]} \n\nФамилия: {user_data[1]} \n\nТелефон: {user_data[2]} \n\nАдрес: {user_data[3]} \n\nВсё верно?", reply_markup=keyboard3)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user_id = call.message.chat.id
    products_id_list = catalog.get_products_id_lists()
    products_id_to_cart = catalog.get_product_id_to_cart()

    if call.data in catalog.categories:
        products = catalog.get_products_list(call.data)

        keyboard_device = types.InlineKeyboardMarkup(row_width=2)
        for j in products:
            item_device = types.InlineKeyboardButton(j[2], callback_data=j[0])
            keyboard_device.row(item_device)

        bot.send_message(call.message.chat.id, 'Выберите устройство', reply_markup=keyboard_device)

    elif call.data in products_id_list:

        keyboard2 = types.InlineKeyboardMarkup(row_width=2)
        item_cart = types.InlineKeyboardButton('В корзину', callback_data=call.data+'cart')
        item_back = types.InlineKeyboardButton('Назад', callback_data='back')
        keyboard2.add(item_back, item_cart)

        device = catalog.get_device(call.data)

        bot.send_photo(call.message.chat.id, open(device[5], 'rb'), '%s \n%s \n\n%s рублей' % (device[2], device[3], device[4]),
                               reply_markup=keyboard2)

    elif call.data == 'back':
        bot.send_message(call.message.chat.id, 'Предлагаю выбрать из списка', reply_markup=main_menu())

    elif call.data in products_id_to_cart:
        cart.add_to_cart(user_id, call.data[:-4])
        add_product = cart.name_add_to_cart(call.data[:-4])

        bot.send_message(call.message.chat.id, f'Супер! {add_product[1]} - отличный выбор!')

    elif call.data == 'yes_order':
        button = types.ReplyKeyboardMarkup(True, True)
        button.row('Да, конечно!')

        bot.send_message(call.message.chat.id, 'Спасибо за Ваш заказ!', reply_markup=button)

        result_user_data = order.check_user_data(user_id)
        result_user_products = cart.show_cart(user_id)
        result = order.send_user_data(result_user_data, result_user_products)
        bot.send_message(config.test_id, result)  # отправка данных менеджеру
        cart.clear_cart(user_id)

    elif call.data == 'no_order':
        bot.send_message(call.message.chat.id, "Введите имя")
        bot.register_next_step_handler(call.message, get_name)

    elif call.data == 'clearing':
        cart.clear_cart(user_id)
        bot.send_message(call.message.chat.id, "Ваша корзина пуста")

    elif call.data == 'ordering':
        user_data = order.check_user_data(call.message.chat.id)

        if user_data:
            user_data_output(call.message.chat.id, user_data)

        else:
            order.get_user_id(call.message.chat.id)

            bot.send_message(call.message.chat.id, "Введите имя")
            bot.register_next_step_handler(call.message, get_name)


def get_name(message):
    if message.text not in ['/start', 'Добавить позицию']:
        order.add_users_data_list(message.text)
        bot.send_message(message.chat.id, 'Введите фамилию')
        bot.register_next_step_handler(message, get_surname)
    else:
        welcome(message)


def get_surname(message):
    if message.text not in ['/start', 'Добавить позицию']:
        order.add_users_data_list(message.text)
        bot.send_message(message.chat.id, 'Введите номер телефона')
        bot.register_next_step_handler(message, get_phone)
    else:
        welcome(message)


def get_phone(message):
    if message.text not in ['/start', 'Добавить позицию']:
        order.add_users_data_list(message.text)
        bot.send_message(message.chat.id, 'Введите адрес')
        bot.register_next_step_handler(message, get_address)
    else:
        welcome(message)


def get_address(message):
    if message.text not in ['/start', 'Добавить позицию']:
        order.add_users_data_list(message.text)
        order.add_users_data_in_db(order.users_data_list, message.chat.id)
        user_data_output(message.chat.id, order.check_user_data(message.chat.id))
    else:
        welcome(message)


def get_category(message):
    if message.text not in ['/start', 'Добавить позицию']:
        if message.text in catalog.categories:
            catalog.add_products_list(message.text)
            bot.send_message(message.chat.id, 'Введите название')
            bot.register_next_step_handler(message, get_product_name)
        else:
            bot.send_message(message.chat.id, 'Такой категории не существует. '
                                              'Доступные категории: %s\n\nВведите категорию' % (' '.join(catalog.categories)))
            bot.register_next_step_handler(message, get_category)
    else:
        welcome(message)


def get_product_name(message):
    if message.text not in ['/start', 'Добавить позицию']:
        catalog.add_products_list(message.text)
        bot.send_message(message.chat.id, 'Введите описание устройства')
        bot.register_next_step_handler(message, get_description)
    else:
        welcome(message)


def get_description(message):
    if message.text not in ['/start', 'Добавить позицию']:
        catalog.add_products_list(message.text)
        bot.send_message(message.chat.id, 'Введите цену')
        bot.register_next_step_handler(message, get_product_price)
    else:
        welcome(message)


def get_product_price(message):
    if message.text not in ['/start', 'Добавить позицию']:
        catalog.add_products_list(message.text)
        bot.send_message(message.chat.id, 'Отправьте картинку')
        bot.register_next_step_handler(message, get_product_image)
    else:
        welcome(message)


def get_product_image(message):
    if message.text not in ['/start', 'Добавить позицию']:
        file_info = bot.get_file(message.photo[0].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        image = os.path.join(catalog.BASE_DIR, 'pictures', "new_image.jpg")
        catalog.add_products_list(image)
        catalog.write_image(downloaded_file, image)
        bot.send_photo(message.chat.id, open(image, 'rb'), "\n%s \n%s \n\n%s рублей\nУстройство добавлено" % (catalog.products_list[1], catalog.products_list[2], catalog.products_list[3]))
        catalog.add_products_in_db(catalog.products_list)
        admin_button(message)
    else:
        welcome(message)


if __name__ == '__main__':
    bot.polling()
