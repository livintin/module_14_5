# -*- coding: utf-8 -*-
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button10 = KeyboardButton(text="Регистрация")
button = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
button5 = KeyboardButton(text="Купить")
kb.row(button, button2, button5, button10)

in_kb = InlineKeyboardMarkup(resize_keyboard=True)
button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
in_kb.add(button3, button4)

in_kb_2 = InlineKeyboardMarkup(resize_keyboard=True)
button6 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button7 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button8 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button9 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
in_kb_2.add(button6, button7, button8, button9)
products = get_all_products()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()



@dp.message_handler(text="Привет!")
async def urban_message(message):
    await message.answer('Введите команду /start, чтобы начать общение')


@dp.message_handler(commands=['start'])
async def urban_message(message):
    print("Start")
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    bool = is_included(message.text)
    if bool is False:
        await state.update_data(username = message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя:")
        await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email = message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_email(message, state):
    await state.update_data(age = message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])

    await message.answer("Регистрация прошла успешно", reply_markup=kb)
    await state.finish()

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=in_kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;\n'
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()


@dp.message_handler(text="Информация")
async def set_gender(message):
    await message.answer(f"Бот, который помогает пользователю рассчитывать норму калорий"
                         f"в зависимости от его пола, возраста, роста и веса")


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for product in products:
        id, title, description, price = product
        await message.answer(f'Product{id}: {title} | '
                             f'Описание: {description} | '
                             f'Цена: {price}')
        with open(f'files/{id}.jpg', "rb") as img:
            await message.answer_photo(img)
    await message.answer("Выберите продукт для покупки:", reply_markup=in_kb_2)

@dp.callback_query_handler(text="product_buying")
async def back(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_gender(call):
    await call.message.answer("Для корректного расчета калорий, укажите свой пол (F/M):")
    await UserState.gender.set()
    await call.answer()


@dp.message_handler(state=UserState.gender)
async def set_age(message, state):
    gender = message.text.upper()
    if gender not in ['F', 'M']:
        await message.answer("Пожалуйста, укажите корректный пол (F/M):")
        return
    await state.update_data(gender=gender)
    await message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    try:
        await state.update_data(age=int(message.text))
        await message.answer(f"Введите свой рост:")
        await UserState.growth.set()
    except ValueError:
        await message.answer("Пожалуйста, введите корректный возраст числом:")


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    try:
        await state.update_data(growth=float(message.text))
        await message.answer(f"Введите свой вес:")
        await UserState.weight.set()
    except ValueError:
        await message.answer(f"Пожалуйста, введите корректный рост числом:")


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    try:
        await state.update_data(weight=float(message.text))
        data = await state.get_data()
        if data['gender'] == 'M':
            await message.answer(
                f"Ваша норма калорий {10 * data['weight'] + 6.25 * data['growth'] + 5 * data['age'] + 5}")
            await state.finish()
        else:
            await message.answer(
                f"Ваша норма калорий {10 * data['weight'] + 6.25 * data['growth'] + 5 * data['age'] - 161}")
            await state.finish()
    except ValueError:
        await message.answer(f"Пожалуйста, введите корректный вес числом:")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
