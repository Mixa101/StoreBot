from aiogram import Dispatcher, types
from db import db_main
from handlers.send_products import making_caption
from aiogram.dispatcher.filters import Text
import buttons

async def show_all_products(message : types.Message):
    products = db_main.get_all_products()
    if products:
        for product in products:
            caption = making_caption(product)
            keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
            keyboard.add(types.InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_{product['product_id']}"))
            await message.answer_photo(photo=product["photo"], caption=caption, reply_markup=keyboard)
        await message.answer("Все что есть в базе", reply_markup=buttons.buy_keyboard)
    else:
        await message.answer("Пока что никто ничего не продает((", reply_markup=buttons.buy_keyboard)

async def add_new_product(call : types.CallbackQuery):
    product_id = call.data.split("_")[1]
    db_main.set_new_product_for_basket(call.from_user.id, product_id)
    await call.message.answer("Товар успешно добавлен в корзинку!", reply_markup=buttons.buy_keyboard)

async def show_basket(message : types.Message):
    basket = db_main.get_products_in_basket(message.from_user.id)
    if basket:
        price_count = 0
        for product in basket:
            price_count += int(product["price"])
            caption = making_caption(product)
            await message.answer_photo(photo=product["photo"], caption=caption)
        await message.answer(f"Общая сумма : {price_count}", reply_markup=buttons.buy_keyboard)
    else:
        await message.answer("Пока что ваша корзинка пуста", reply_markup=buttons.buy_keyboard)
    
def register_buyer_handlers(dp : Dispatcher):
    dp.register_message_handler(show_all_products, Text(equals="Товары"))
    dp.register_callback_query_handler(add_new_product, Text(startswith="add_"))
    dp.register_message_handler(show_basket, Text(equals="Корзина"))