from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(row_width=2,
                                 inline_keyboard=[
                                     [
                                        InlineKeyboardButton(text='Профиль', callback_data='profile'),
                                        InlineKeyboardButton(text='Настройки', callback_data='setting')
                                     ],
                                     [
                                        InlineKeyboardButton(text='Найти собеседника', callback_data='search')
                                     ]
                                 ])
