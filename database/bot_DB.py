import random
import sqlite3
from config import bot


def sql_create():
    global db, cursor
    db = sqlite3.connect('bot.sqlite3')
    cursor = db.cursor()
    if db:
        print('база данныз подключена')
    db.execute("CREATE TABLE IF NOT EXISTS menu "
               "(id INTEGER PRIMARY KEY, photo TEXT, dish TEXT, des INTEGER , price INTEGER )")
    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO menu VALUES (?,?,?,?,?)", tuple(data.values))
        db.commit()


async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM menu").fetchall()
    r_u = random.randint(0, len(result) - 1)
    await bot.send_photo(message.from_user.id, result[r_u][1])
    await bot.send_message(message.from_user.id, f"photo{result[r_u][2]}"
                                                 f"dish{result[r_u][3]}"
                                                 f"des{result[r_u][4]}"
                                                 f"price{result[r_u][5]}"
                                                 f"{result[r_u][0]}")


async def sql_command_all(message):
    return cursor.execute("SELECT * FROM menu").fetchall()


async def sql_command_delete(id):
    cursor.execute("DELETE FROM menu WHERE id == ?", (id,))
    db.commit()
