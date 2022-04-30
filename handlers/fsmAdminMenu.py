from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .keyboards import cancel_markup
from config import bot, ADMIN
from database import bot_DB


class FCMAdmin(StatesGroup):
    photo = State()
    dish = State()
    des = State()
    price = State


async def fsm_start(message: types.Message):
    if message.chat.type == 'private':
        await FCMAdmin.photo.set()
        await bot.send_message(message.chat.id,
                               f"Send {message.from_user.full_name}, photo",
                               reply_markup=cancel_markup)
    else:
        await message.answer("В личку мне пиши!")


async def photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['users'] = message.from_user.username
        data['photo'] = message.photo[0].file_id
    await FCMAdmin.next()
    await message.reply('name dish')


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['dish_name'] = message.text
    await FCMAdmin.next()
    await message.reply('description of the dish')


async def load_Des(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Description'] = message.text
    await FCMAdmin.next()
    await message.reply('tell me the price')


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
    # async with state.proxy() as data:
    #     await bot.send_message(message.chat.id, str(data))
    await bot_DB.sql_command_insert(state)
    await state.finish()
    await bot.send_message(message.chat.id, 'okey')


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.reply('OK!')


async def delete_data(message: types.Message):
    if message.from_user.id == ADMIN:
        results = await bot_DB.sql_command_all(message)
        for result in results:
            await bot.send_message(message.from_user.id, f"photo{result[2]}"
                                                         f"dish{result[3]}"
                                                         f"des{result[4]}"
                                                         f"price{result[5]}"
                                                         f"{result[0]}"),
            reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(
                f"delete:{result[0]}"
            ))
    else:
        await message.answer("ты не админ")


async def complete_delete(call: types.CallbackQuery):
    await bot_DB.sql_command_delete(call.data.replace("delete:", ""))
    await call.answer(text=f"{call.data.replace('delete:', '')} deleted", show_alert=True)


def register_hendler_fsmAdminGetUser(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands=["go"])
    dp.register_message_handler(cancel_reg, state="*", commands="cancel")
    dp.register_message_handler(cancel_reg, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(photo, state=FCMAdmin.photo, content_types=["photo"])
    dp.register_message_handler(load_name, state=FCMAdmin.dish)
    dp.register_message_handler(load_Des, state=FCMAdmin.des)
    dp.register_message_handler(load_price, state=FCMAdmin.price)

    dp.register_message_handler(delete_data, commands=['delete'])
    dp.register_callback_query_handler(complete_delete,
                                       lambda call: call.data and call.data.startswith("delete"))
