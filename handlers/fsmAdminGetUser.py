from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .keyboards import cancel_markup
from config import bot, ADMIN
from database import bot_DB


# states
class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    surname = State()
    age = State()
    region = State()


# start fsm
async def fsm_start(message: types.Message):
    if message.chat.type == 'private':
        await FSMAdmin.photo.set()
        await bot.send_message(message.chat.id,
                               f"Привет {message.from_user.full_name}, скинь фотку...",
                               reply_markup=cancel_markup)
    else:
        await message.answer("В личку мне пиши!")


# load photo
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['nickname'] = f"@{message.from_user.username}"
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, "Как зовут?")


# load name
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, "Какая фамилия?")


# load surname
async def load_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, "Сколько лет(только числа)?")


async def load_age(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['age'] = int(message.text)
        await FSMAdmin.next()
        await bot.send_message(message.chat.id, "Где живешь?")
    except:
        await bot.send_message(message.chat.id, "Я сказал только числа!!!")


# load region
async def load_region(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['region'] = message.text
    # async with state.proxy() as data:
    #     await bot.send_message(message.chat.id, str(data))
    await bot_DB.sql_command_insert(state)
    await state.finish()
    await bot.send_message(message.chat.id, "Все свободен)")


async def cancal_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.reply("ОК")


async def delete_data(message: types.Message):
    if message.from_user.id == ADMIN:
        results = await bot_DB.sql_command_all(message)
        for result in results:
            await bot.send_photo(message.from_user.id, result[2],
                                 caption=f"Name: {result[3]}\n"
                                         f"Surname: {result[4]}\n"
                                         f"Age: {result[5]}\n"
                                         f"Region: {result[6]}\n\n"
                                         f"{result[1]}",
                                 reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                     f"delete: {result[3]}",
                                     callback_data=f"delete: {result[0]}"
                                 )))
    else:
        await message.answer("Ты не админ!!!")


async def complete_delete(call: types.CallbackQuery):
    await bot_DB.sql_command_delete(call.data.replace('delete: ', ''))
    await call.answer(text=f"{call.data.replace('delete: ', '')} deleted", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


def register_hendler_fsmAdminGetUser(dp: Dispatcher):
    dp.register_message_handler(cancal_reg, state="*", commands="cancel")
    dp.register_message_handler(cancal_reg, Text(equals='cancel', ignore_case=True), state="*")

    dp.register_message_handler(fsm_start, commands=["register"])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=["photo"])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_surname, state=FSMAdmin.surname)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_region, state=FSMAdmin.region)

    dp.register_message_handler(delete_data, commands=['delete'])
    dp.register_callback_query_handler(complete_delete,
                                       lambda call: call.data and call.data.startswith("delete: "))
