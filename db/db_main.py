import sqlite3
from aiogram.types import Message
from db import queries
import buttons

db = sqlite3.connect('db/store.sqlite3')
db.row_factory = sqlite3.Row
cursor = db.cursor()


async def sql_create():
    if db:
        print('data base is ready!')
    
    
    cursor.execute(queries.CREATE_TABLE_STORE)
    cursor.execute(queries.CREATE_TABLE_PRODUCT_DETAILS)
    cursor.execute(queries.CREATE_TABLE_COLLECTION_PRODUCTS)
    cursor.execute(queries.CREATE_TABLE_USERS)
    cursor.execute(queries.CREATE_TABLE_BASKET)

async def sql_insert_product(product_id, product_name, size, price, photo, category, info_product, collection, user_id):
    cursor.execute(queries.INSERT_DETAILS_QUERY, (product_id, category, info_product, user_id))
    cursor.execute(queries.INSERT_STORE_QUERY, (product_id, product_name, size, price, photo, user_id))
    cursor.execute(queries.INSERT_COLLECTION_QUERY, (product_id, collection, user_id))
    db.commit()

def fetch_all_products(user_id : int):
    products = cursor.execute(queries.GET_ALL_PRODUCTS, (user_id, )).fetchall()
    products_list = [dict(product) for product in products]
    return products_list

def user_exists(message : Message):
    user = cursor.execute(queries.CHECK_USER_EXISTS, (int(message.from_user.id), )).fetchall()
    if user:
        return True
    return False

def create_user(id, user_type):
    cursor.execute(queries.INSERT_USERS_QUERY, (id, user_type))
    db.commit()

def check_user_type(message : Message):
    user_type = cursor.execute(queries.CHECK_USER_TYPE, (message.from_user.id, )).fetchone()
    if user_type["user_type"].lower() == "Продавец".lower():
        return True
    elif user_type["user_type"] == "Покупатель":
        return False

def get_products_in_basket(user_id):
    product_ids = cursor.execute(queries.GET_BASKET, (user_id, )).fetchall()
    product_ids = [item["product_id"] for item in product_ids]
    products = cursor.execute(queries.GET_BASKET_PRODUCTS).fetchall()
    basket = [product for product in products if product["product_id"] in product_ids]
    return basket

def get_all_products():
    products = cursor.execute(queries.GET_BASKET_PRODUCTS).fetchall()
    return products

def set_new_product_for_basket(user_id, product_id):
    cursor.execute(queries.INSERT_BASKET_QUERY, (user_id, product_id))
    db.commit()