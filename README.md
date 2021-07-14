# TELEGRAM-BOT "XIAOMI STORE"

Telegram store is a telegram bot allowing to sell xiaomi products stored in data base to user.

## Usage:
```python
python main.py
```

## User interface
This bot displays the products of the Xiaomi store that are stored in the database.
The user can view all products, depending on the category, add the desired ones
to the cart and place an order. Then the user fills in the data about himself,
if he has already bought in this store, then he checks the data.
Then the data about the user is sent to the admin.

<img src="https://github.com/SnezhanaM/Telegram-store/blob/main/pictures/user_interface.gif" width="210" height="400"/>


## Admin interface
You need change the test_id in config.py to your own, to enter from the admin page.
The admin can manually enter product data.
It also receives data about customer orders.
All customer data is stored in users.db.
The library sqlite3 is used to work with databases.

<img src="https://github.com/SnezhanaM/Telegram-store/blob/main/pictures/admin_interface.gif" width="210" height="400"/>

