CREATE_TABLE_STORE = """
CREATE TABLE IF NOT EXISTS store (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    user_id INTEGER,
    product_id INTEGER,
    name_product varchar(255),
    size varchar(255),
    price varchar(255),
    photo TEXT
)
"""

CREATE_TABLE_PRODUCT_DETAILS = """
CREATE TABLE IF NOT EXISTS product_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    category varchar(255),
    info_product varchar(255)
)
"""

CREATE_TABLE_COLLECTION_PRODUCTS = """
    CREATE TABLE IF NOT EXISTS collection_products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        collection varchar(255)
    )
"""
CREATE_TABLE_USERS = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_type VARCHAR(255)
    )
"""

CREATE_TABLE_BASKET = """
    CREATE TABLE IF NOT EXISTS basket (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER
    )
"""

INSERT_BASKET_QUERY = """
    INSERT INTO basket (user_id, product_id)
    VALUES (?, ?)
"""

INSERT_USERS_QUERY = """
    INSERT INTO users (user_id, user_type)
    VALUES (?, ?)
"""

INSERT_STORE_QUERY = """
    INSERT INTO store (product_id, name_product, size, price, photo, user_id)
    VALUES (?, ?, ?, ?, ?, ?)
"""

INSERT_DETAILS_QUERY = """
    INSERT INTO product_details (product_id, category, info_product, user_id)
    VALUES (?, ?, ?, ?)
"""

INSERT_COLLECTION_QUERY = """
    INSERT INTO collection_products (product_id, collection, user_id)
    VALUES (?, ?, ?)
"""

GET_ALL_PRODUCTS = """
    SELECT s.id, s.product_id, s.name_product, s.size, s.price,
    s.photo, ds.category, ds.info_product, cs.collection
    FROM store s
    INNER JOIN product_details ds ON s.product_id = ds.product_id
    INNER JOIN collection_products cs ON s.product_id = cs.product_id
    WHERE s.user_id = ?
"""

GET_BASKET_PRODUCTS = """
    SELECT s.id, s.product_id, s.name_product, s.size, s.price,
    s.photo, ds.category, ds.info_product, cs.collection
    FROM store s
    INNER JOIN product_details ds ON s.product_id = ds.product_id
    INNER JOIN collection_products cs ON s.product_id = cs.product_id
"""

GET_BASKET = """
    SELECT b.product_id FROM basket b WHERE b.user_id = ?;
"""

CHECK_USER_EXISTS = """
    SELECT u.user_id FROM users u WHERE u.user_id = ?;
"""

CHECK_USER_TYPE = """
    SELECT u.user_type FROM users u WHERE u.user_id = ?;
"""