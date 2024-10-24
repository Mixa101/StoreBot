from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from buttons import sizes_keyboard, sizes, cancel, yes_or_no
from db.db_main import sql_insert_product, check_user_type

# создаем состояния для управления вводом данных
class fsm_store(StatesGroup):
    product_name = State() 
    size = State()
    category = State()
    price = State()
    photo = State()
    info = State()
    product_id = State()
    collection = State()
    data_correction = State()

# обработчик кнопки отмены
async def cancel_fsm(message : types.Message, state: FSMContext):
    if await state.get_state() is not None:
        await state.finish()
        await message.answer("Отменено", reply_markup=ReplyKeyboardRemove())
        
# начало поиска
async def start_product(message : types.Message):
    await message.answer("введите название товара:", reply_markup = cancel)
    await fsm_store.product_name.set()

# ввод названия
async def load_product_name(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['product_name'] = message.text
    await message.answer("Введите нужный размер:", reply_markup=sizes_keyboard)
    await fsm_store.next()

# ввод размера
async def load_size(message : types.Message, state : FSMContext):
    if message.text in sizes: # исключаем другие размеры которых не существует
        async with state.proxy() as data:
            data['size'] = message.text
        await message.answer("Выберите категорию:", reply_markup=cancel)
        await fsm_store.next()
    else: # в случае неправильного ввода
        await message.answer(f"У нас нет такого размера!\n"
                            "выберите из кнопки!", reply_markup=sizes_keyboard)

# ввод категорий
async def load_category(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    
    await message.answer("Введите цену:")
    await fsm_store.next()

# ввод цены
async def load_price(message : types.Message, state : FSMContext):
    if message.text.isnumeric(): # проверяем сообщение на правильность (ну цена же не может быть из букв XD)
        async with state.proxy() as data:
            data['price'] = int(message.text)
    
        await message.answer("Фото товара: ")
        await fsm_store.next()
    else:
        await message.answer("Цена должна состоять из цифр!")

# отправка фото
async def load_photo(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
    
    await message.answer("Введите информацию про продукт!")
    await fsm_store.next()
    
async def load_info(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['info'] = message.text
    await message.answer("Введите уникальное значение для этого товара:")
    await fsm_store.next()

async def load_id(message : types.Message, state : FSMContext):
    if message.text.isnumeric():
        async with state.proxy() as data:
            data['id'] = int(message.text)
        
        await message.answer("Введите коллекцию: ")
        await fsm_store.next()

    else:
        await message.answer("уникальное значение должно состоять из цифр!")

async def get_collection(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['collection'] = message.text

        await message.answer_photo(photo=data["photo"],
                                caption=f'Ваш товар:\n'
                                f'Название товара: {data["product_name"]}\n'
                                f'Размер: {data["size"]}\n'
                                f'Категория: {data["category"]}\n'
                                f'Цена: {data["price"]}\n'
                                f'инфо: {data["info"]}\n'
                                f'уникальное значение: {data["id"]}\n'
                                f'коллекция: {data["collection"]}',
                                reply_markup=ReplyKeyboardRemove())
        await message.answer("Все верно?", reply_markup=yes_or_no)
        await fsm_store.next()

# здесь обрабатываем "Да" "Нет"
async def correct_data(message : types.Message, state : FSMContext):
    if message.text.lower() == 'да':
        async with state.proxy() as data:
            await sql_insert_product(data['id'], data['product_name'], data['size'],
                                     data['price'], data['photo'], data['category'], 
                                     data['info'], data['collection'], message.from_user.id)
        await message.answer('Сохранено в базу',
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()
    elif message.text.lower() == 'нет':
        await message.answer("Введите название товара: ")
        await fsm_store.product_name.set()
    else:
        await message.answer("не понял 'да' или 'нет'?", reply_markup=yes_or_no)

def register_store_handlers(dp : Dispatcher):
    # ниже регистрируем все что есть и указываем все фильтры
    dp.register_message_handler(cancel_fsm, Text(equals="Отмена", ignore_case=True),state='*')
    dp.register_message_handler(start_product, Text(equals="Добавить товар"), check_user_type)
    dp.register_message_handler(load_product_name, state=fsm_store.product_name)
    dp.register_message_handler(load_size, state=fsm_store.size)
    dp.register_message_handler(load_category, state=fsm_store.category)
    dp.register_message_handler(load_price, state=fsm_store.price)
    dp.register_message_handler(load_photo, state=fsm_store.photo, content_types=['photo'])
    dp.register_message_handler(load_info, state=fsm_store.info)
    dp.register_message_handler(load_id, state=fsm_store.product_id)
    dp.register_message_handler(get_collection, state=fsm_store.collection)
    dp.register_message_handler(correct_data, state=fsm_store.data_correction)
