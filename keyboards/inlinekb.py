from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

reg_menu = InlineKeyboardBuilder()
reg_menu.add(types.InlineKeyboardButton(text='Register', callback_data='register'))

levels = InlineKeyboardBuilder()
levels.row(types.InlineKeyboardButton(text='A1\n(Beginner)', callback_data='A1'),
           types.InlineKeyboardButton(text='A2\n(Elementary)', callback_data='A2'))
levels.row(types.InlineKeyboardButton(text='B1\n(Intermediate)', callback_data='B1'),
           types.InlineKeyboardButton(text='B2\n(Upper Intermediate)', callback_data='B2'))
levels.row(types.InlineKeyboardButton(text='C1\n(Advanced)', callback_data='C1'),
           types.InlineKeyboardButton(text='C2\n(Proficiency)', callback_data='C2'))

to_menu = InlineKeyboardBuilder()
to_menu.add(types.InlineKeyboardButton(text='Main menu', callback_data='main'))

main_menu = InlineKeyboardBuilder()
main_menu.row(
    types.InlineKeyboardButton(text="Profile", callback_data='profile'),
    types.InlineKeyboardButton(text="Settings", callback_data='settings')
)
main_menu.row(types.InlineKeyboardButton(
    text="Find a companion", callback_data='search')
)

setting_kb = InlineKeyboardBuilder()
setting_kb.add(types.InlineKeyboardButton(text='Change Level', callback_data='change_level'))
setting_kb.add(types.InlineKeyboardButton(text='Change About', callback_data='change_about'))
setting_kb.row(types.InlineKeyboardButton(text='Back', callback_data='main'))


reg_levels = InlineKeyboardBuilder()
reg_levels.row(types.InlineKeyboardButton(text='A1\n(Beginner)', callback_data='change_to_A1'),
               types.InlineKeyboardButton(text='A2\n(Elementary)', callback_data='change_to_A2'))
reg_levels.row(types.InlineKeyboardButton(text='B1\n(Intermediate)', callback_data='change_to_B1'),
               types.InlineKeyboardButton(text='B2\n(Upper Intermediate)', callback_data='change_to_B2'))
reg_levels.row(types.InlineKeyboardButton(text='C1\n(Advanced)', callback_data='change_to_C1'),
               types.InlineKeyboardButton(text='C2\n(Proficiency)', callback_data='change_to_C2'))
reg_levels.row(types.InlineKeyboardButton(text='Back', callback_data='main'))

only_back = InlineKeyboardBuilder()
only_back.add(types.InlineKeyboardButton(text='Back', callback_data='main'))
