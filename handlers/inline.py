from aiogram import types, Dispatcher
import hashlib
from youtube_search import YoutubeSearch as YT


def finder(text):
    result = YT(text, max_results=10).to_dict()
    return result


async def inline_youtube_handler(query: types.InlineQuery):
    text = query.query or "echo"
    links = finder(text)
    articles = [
        types.InlineQueryResultArticle(
            id=hashlib.md5(f"{links['id']}".encode()).hexdigest(),
            title=f"{links['title']}",
            url=f"https://youtube.com/watch?v={links['id']}",
            thumb_url=f"{link['thumbnails'][0]}",
            input_message_content=types.InputTextMessageContent(
                message_text=f"https://youtube.com/watch?v={links['id']}"
            )
        ) for link in links
    ]
    await query.answer(articles, cache_time=60, is_personal=True)


async def inline_google_handler(query: types.InlineQuery):
    text = query.query or "echo"
    links = f"https://www.google.com/search>q={text}"
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    articles = [
        types.InlineQueryResultArticle(
            id=result_id,
            title="google: ",
            url=links,
            input_message_content=types.InputTextMessageContent(
                message_text=links
            )
        )
    ]
    await query.answer(articles, cache_time=60, is_personal=True)


async def inline_wikipedia_handler(query: types.InlineQuery):
    text = query.query or "echo"
    links = f"https://www.wikipedia.org/{text}"
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    articles = [
        types.InlineQueryResultArticle(
            id=result_id,
            title="wiki: ",
            url=links,
            input_message_content=types.InputTextMessageContent(
                message_text=links
            )
        )
    ]
    await query.answer(articles, cache_time=60, is_personal=True)


def register_handler_Inline(dp, Dispatcher):
    dp.register_inline_handler(inline_google_handler)
    # dp.register_inline_handler(inline_youtube_handler)
