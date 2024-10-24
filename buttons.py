from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# создаем кнопки с размерами
sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
size_buttons = [KeyboardButton(text=i) for i in sizes] # используем list comprehensions для создания кнопок
sizes_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

for i in range(0, len(sizes), 3): # используем шаг в 3 для того чтобы вместить по 3 кнопки в ряд
    sizes_keyboard.add(size_buttons[i], size_buttons[i+1], size_buttons[i+2]) #Добавляем кнопки

# создаем кнопку для отмены 
cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_button = KeyboardButton('Отмена')
cancel.add(cancel_button)

# создаем кнопки с ответами "Да" "Нет"
yes_or_no = ReplyKeyboardMarkup(resize_keyboard=True)
yes_or_no_buttons = [KeyboardButton(text='Да'), KeyboardButton(text='Нет')]
yes_or_no.add(yes_or_no_buttons[0], yes_or_no_buttons[1])

# buyer buttons
buy_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
show_products_button = KeyboardButton(text="Товары")
basket_button  = KeyboardButton(text="Корзина")
buy_keyboard.add(show_products_button, basket_button)

# seller buttons
seller_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
new_product = KeyboardButton(text="Добавить товар")
show_my_product = KeyboardButton(text="Показать мои товары")
seller_keyboard.add(new_product, show_my_product)

# send_one buttons
def create_buttons(product_id):
    delete_button = InlineKeyboardButton('Удалить', callback_data=f'delete_{product_id}')
    next_button = InlineKeyboardButton('Следующий', callback_data='next')
    cancel_btn = InlineKeyboardButton('Отмена', callback_data='cancel')
    edit_button = InlineKeyboardButton('Редактировать', callback_data=f"edit_{product_id}")
    prev_button = InlineKeyboardButton('Прошлый', callback_data='back')
    return [next_button, delete_button, edit_button, cancel_btn, prev_button]