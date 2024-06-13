from aiogram.types import CallbackQuery
from aiogram import Router, F, Bot

from keyboards.inlinekb import main_menu, setting_kb, levels

router = Router()


@router.callback_query(F.data == 'main')
async def delete_msg(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Main menu", reply_markup=main_menu.as_markup())


@router.callback_query(F.data == 'settings')
async def show_inline_menu(call: CallbackQuery):
    await call.message.edit_text('Settings', reply_markup=setting_kb.as_markup())


@router.callback_query(F.data == 'change_level')
async def show_inline_menu(call: CallbackQuery):
    await call.message.edit_text('Levels', reply_markup=levels.as_markup())


@router.callback_query(F.data == 'change_about')
async def show_inline_menu(call: CallbackQuery):
    await call.message.edit_text('Write me your bio')
