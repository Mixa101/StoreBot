import sqlite3
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db.db_main import fetch_all_products

class Edit_product(StatesGroup):
    for_field = State()
    for_new_value = State()
    for_photo = State()

def get_db_connection():
    conn = sqlite3.connect('db/store.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn


def update_product_field(product_id, field_name, new_value):
    store_table = ["name_product", "size", "price", "photo"]
    product_details_table = ["category","info_product"]
    collection_table = ["collection"]
    
    conn = get_db_connection()
    
    try:
        if field_name in store_table:
            query = f"UPDATE store SET {field_name} = ? WHERE product_id = ?"
        elif field_name in product_details_table:
            query = f"UPDATE product_details SET {field_name} = ? WHERE product_id = ?"
        elif field_name in collection_table:
            query = f"UPDATE collection_products SET {field_name} = ? WHERE product_id = ?"
        else:
            raise ValueError(f"Нет такого поля {field_name}")
        
        conn.execute(query, (new_value, product_id))
        conn.commit()
    
    except sqlite3.OperationalError as e:
        print(f"Ошибка - {e}")
    finally:
        conn.close()

async def start_edit_product(call : types.CallbackQuery, state : FSMContext):
    await state.update_data(product_id = call.data.split("_")[1])
    fields_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    fields = fetch_all_products(call.from_user.id)
    fields = [key for key, value in fields[0].items()]
    fields = fields[2:]
    await state.update_data(fields = fields)
    fields = [types.KeyboardButton(text=f"{field}") for field in fields]
    fields_keyboard.add(*fields)
    await call.message.answer("Выберите какое поле будете менять: ", reply_markup=fields_keyboard)
    await Edit_product.for_field.set()

async def get_field(message : types.Message, state : FSMContext):
    fields = await state.get_data()
    fields = fields.get("fields")
    if message.text not in fields:
        await message.answer(f"У нас нет такого поля {message.text}")
        return
    
    await state.update_data(field = message.text)
    
    if message.text == 'photo':
        await message.answer("Отправьте фото")
        await Edit_product.for_photo.set()
    else:
        await message.answer("Отправьте новое значение")
        await Edit_product.for_new_value.set()

async def set_new_value(message : types.Message, state : FSMContext):
    user_data = await state.get_data()
    product_id = user_data['product_id']
    field = user_data['field']
    new_value = message.text
    update_product_field(product_id, field, new_value)
    await message.answer(f"Поле {field} успешно обновлено")
    await state.finish()

async def set_new_photo(message : types.Message, state : FSMContext):
    user_data = await state.get_data()
    product_id = user_data['product_id']
    photo_id = message.photo[-1].file_id
    
    update_product_field(product_id, 'photo', photo_id)

    await message.answer('Фото успешно обновлено!')
    await state.finish()