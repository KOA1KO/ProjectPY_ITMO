from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel_kb = [
    [KeyboardButton(text="/cancel")]
]
get_cancel_kb = ReplyKeyboardMarkup(keyboard=cancel_kb, resize_keyboard=True)
