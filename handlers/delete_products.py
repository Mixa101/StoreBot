from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import InputMediaPhoto
from db import db_main
import sqlite3

def delete_product(product_id):
    conn = sqlite3.connect('db/store.sqlite3')
    conn.execute("DELETE FROM store WHERE product_id = ?", (product_id,))
    conn.execute("DELETE FROM product_details WHERE product_id = ?", (product_id,))
    conn.execute("DELETE FROM collection_products WHERE product_id = ?", (product_id,))
    conn.commit()
    conn.close()

async def delete_product_callback(call : types.CallbackQuery):
    product_id = int(call.data.split('_')[1])
    
    delete_product(product_id)
    
    if call.message.photo:
        new_cap = 'Товар был удален. Обновите список'
        photo_404 = open('img/img_404.jpeg', 'rb')
        
        await call.message.edit_media(
            InputMediaPhoto(media=photo_404,
                            caption=new_cap)
        )
    else:
        await call.message.edit_text('Товар был удален! Обновите список')