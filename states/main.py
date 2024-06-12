from app import dp

from inlinekb import main_menu

from aiogram import types


@dp.message_handler(text='Главное меню')
async def show_inline_menu(message: types.Message):
    await message.answer('Главное меню', reply_markup=main_menu)