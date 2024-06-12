from config import deepl_api_key
import deepl

auth_key = deepl_api_key
translator = deepl.Translator(auth_key)


async def transfer(text):
    result = translator.translate_text(text=text, target_lang="RU")
    return result


async def form(text):
    return text + "\n___\n" + f'<tg-spoiler>{transfer(text)}</tg-spoiler>'
