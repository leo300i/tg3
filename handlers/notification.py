from aiogram import types, Dispatcher
from config import bot, dp
from list import bad_words
import asyncio
import aioschedule


async def wake_up():
    await bot.send_message(chat_id=chat_id, text="get up")


async def scheduler(time):
    aioschedule.every().day.at(time).do(wake_up())
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def echo_message(message: types.Message):
    global chat_id
    chat_id = message.chat.id


    bw = bad_words

    for i in bad_words:
        if i in message.text.lower():
            await message.delete()
            await bot.send_message(message.chat.id,
                                       f"{message.from_user.full_name}, сам ты {i}!!!"
                                       )
    # Send dice
    if message.text.lower() == 'dice':
        await bot.send_dice(message.chat.id, emoji="🎯")

    # not
    if message.text.startswith("wake up"):
        await message.reply("ok")
        await scheduler(message.text.replace("wake up"))


def register_hendlers_notification(dp: Dispatcher):
    dp.register_message_handler(echo_message)
