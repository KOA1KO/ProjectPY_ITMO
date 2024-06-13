from keyboards.inlinekb import main_menu

from aiogram import types, Router, F

router = Router()


@router.message(F.text == 'to_main')
async def show_inline_menu(message: types.Message):
    await message.answer('Главное меню', reply_markup=main_menu)
