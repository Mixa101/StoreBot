from aiogram import executor
import logging
from config import dp
from handlers import fsm_store, send_products, start_handler, send_products_for_buyer
from db import db_main

async def on_startup(_):
    await db_main.sql_create()

fsm_store.register_store_handlers(dp) # регистрируем обработчики
send_products.register_send_products_handler(dp)
start_handler.register_start_handler(dp)
send_products_for_buyer.register_buyer_handlers(dp)


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, allowed_updates=['callback'])