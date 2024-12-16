import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from apikeyBot import api

logging.basicConfig(level=logging.INFO)
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Рассчитать"),
            KeyboardButton(text="Информация"),
            KeyboardButton(text="Купить")
        ]
    ],resize_keyboard=True
)
kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton('Формулы расчёта', callback_data='formulas')],
    ]
)
catalog_kb =  InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Product1', callback_data="product_buying")],
        [InlineKeyboardButton('Product2', callback_data="product_buying")],
        [InlineKeyboardButton('Product3', callback_data="product_buying")],
        [InlineKeyboardButton('Product4', callback_data="product_buying")]
    ]
)
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open('1.bmp', 'rb') as img1:
        await message.answer_photo(img1,'Название: Product1 | Описание: описание 1 | Цена: 100')
    with open('2.bmp', 'rb') as img2:
        await message.answer_photo(img2,'Название: Product2 | Описание: описание 2 | Цена: 200')
    with open('3.bmp', 'rb') as img3:
        await message.answer_photo(img3,'Название: Product3 | Описание: описание 3 | Цена: 300')
    with open('4.bmp', 'rb') as img4:
        await message.answer_photo(img4,'Название: Product4 | Описание: описание 4 | Цена: 400')
    await message.answer('Выберите продукт для покупки:', reply_markup=catalog_kb)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выбери опцию:', reply_markup=kb)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=start_kb)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст: ')
    await UserState.age.set()
    await call.answer


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    f = 'Формула Миффлина-Сан Жеора:\n' \
        'для мужчин: 10 х вес + 6.25 x рост – 5 х возраст + 5\n' \
        'для женщин: 10 x вес + 6.25 x рост – 5 x возраст – 161'
    await call.message.answer(f)


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Я бот, рассчитывающий норму калорий')


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост, пожалуйста')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес, пожалуйста')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = state.get_data
    try:
        calories_man = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
        calories_wom = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
        await message.answer(f'Норма (муж.): {calories_man} ккал')
        await message.answer(f'Норма (жен.): {calories_wom} ккал')
    except:
        await message.answer("Не могу конвертировать ваши значения в числа")
        return 
    await state.finish()




@dp.message_handler()
async def all_messages(message):
    print(f'Получено: {message.text}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
