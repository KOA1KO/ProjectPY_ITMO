from config import deepl_api_key
import deepl

auth_key = deepl_api_key
translator = deepl.Translator(auth_key)


def trans(text: str) -> str:
    res = translator.translate_text(text, target_lang="RU")
    result = text + "\n___\n" + f'<tg-spoiler>{res}</tg-spoiler>'
    return result

