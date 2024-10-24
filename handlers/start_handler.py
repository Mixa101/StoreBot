from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from db import db_main
import buttons

async def start_command(message : types.Message):
    if db_main.user_exists(message):
        if db_main.check_user_type(message):
            keyboard = buttons.seller_keyboard
        else:
            keyboard = buttons.buy_keyboard
        await message.answer("Вы уже зарегестрированы!", reply_markup=keyboard)
        return
    
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.InlineKeyboardButton(text="Покупатель", callback_data="reg_buyer"),
                 types.InlineKeyboardButton(text='Продавец', callback_data='reg_seller'))
    await message.answer("Добро пожаловать выберите кем вы хотите зарегестрироваться!", reply_markup=keyboard)
    
async def start_reg_user(call : types.CallbackQuery):
    user_type = call.data.split('_')[1]
    if user_type == "buyer":
        user_type = "Покупатель"
    else:
        user_type = "Продавец"
        
    db_main.create_user(call.from_user.id, user_type)
    await call.message.edit_text("Успех!")

async def user_exists(message : types.Message):
    await message.answer("Вы уже зарегестрированы!")
    
def register_start_handler(dp : Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_callback_query_handler(start_reg_user, Text(startswith="reg_"))
    