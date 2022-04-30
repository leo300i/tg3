from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types, Dispatcher
from config import bot, dp, ADMIN
from parser import news
from database import bot_DB
from parser import anime


async def mem(message: types.Message):
    photo = open('media/lp1.png', 'rb')
    bot.send_photo(message.chat.id, photo=photo)


# @dp.message_handler(commands=['start'])
async def hello(message: types.Message):
    await bot.send_message(message.chat.id, f"Салам хозяин {message.from_user.full_name}")


# @dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    question = "Какого типа данных не существует в Python?"
    answers = ['int', 'str', 'elif', 'tuple']
    await bot.send_poll(message.chat.id,
                        question=question,
                        options=answers,
                        is_anonymous=False,
                        type='quiz',
                        correct_option_id=2
                        )


# @dp.message_handler(commands=['problem'])
async def problem_1(message: types.Message):
    murkup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton(
        "NEXT",
        callback_data="button_call_1"
    )
    murkup.add(button_call_1)

    photo = open("media/problem1.jpg", "rb")
    await bot.send_photo(message.chat.id, photo=photo)

    question = "Output:"
    answers = ["[2, 4]", '[2, 4, 6]', '[2]', '[4]', '[0]', "Error"]
    await bot.send_poll(message.chat.id,
                        question=question,
                        options=answers,
                        is_anonymous=False,
                        type='quiz',
                        correct_option_id=0,
                        open_period=5,
                        reply_markup=murkup
                        )


# @dp.message_handler(commands=["ban"], commands_prefix="!/")
async def ban(message: types.Message):
    if message.chat.type != "private":
        if message.from_user.id != ADMIN:
            await message.reply("Ты не мой БОСС!")

        if not message.reply_to_message:
            await message.reply("Команда должна быть ответом на сообщение!")

        else:
            await message.bot.delete_message(message.chat.id, message.message_id)
            await message.bot.kick_chat_member(message.chat.id, user_id=message.reply_to_message.from_user.id)
            await bot.send_message(
                message.chat.id,
                f"{message.reply_to_message.from_user.full_name} забанен по воле {message.from_user.full_name}")


    else:
        await message.answer("Это работает только в группах!")


async def show_random_user(message: types.Message):
    await bot_DB.sql_command_random(message)


async def parser_anime(message: types.Message):
    data = anime.parser()
    for item in data:
        await  bot.send_message(message.chat.id, item)


async def parser_news(message: types.Message):
    data = news.parser()
    for item in data:
        await bot.send_message(message.chat.id, item)


def register_hendlers_client(dp: Dispatcher):
    dp.register_message_handler(mem, commands=["mem"])
    dp.register_message_handler(hello, commands=["start"])
    dp.register_message_handler(quiz_1, commands=["quiz"])
    dp.register_message_handler(problem_1, commands=["problem"])
    dp.register_message_handler(ban, commands=["ban"], commands_prefix="!/")
    dp.register_message_handler(show_random_user, commands=["random"])
    dp.register_message_handler(parser_anime, commands=["anime"])
    dp.register_message_handler(parser_news, commands=["news"])
