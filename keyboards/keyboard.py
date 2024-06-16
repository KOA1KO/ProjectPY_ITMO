from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

skip_companion = ReplyKeyboardBuilder()
skip_companion.add(types.KeyboardButton(text='Quit the conversation'))

cancel_kb = ReplyKeyboardBuilder()
cancel_kb.add(types.KeyboardButton(text='/cancel'))