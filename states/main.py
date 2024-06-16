import asyncio

import aiogram
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram import Router, F, Bot

from data.base import update_is_searching, is_someone_searching, get_profile, update_level
from keyboards.inlinekb import main_menu, setting_kb, reg_levels, only_back
from keyboards.keyboard import skip_companion

router = Router()


class MenuStatesGroup(StatesGroup):
    level_reg = State()
    search = State()


@router.callback_query(F.data == 'main')
async def delete_msg(call: CallbackQuery):
    await update_is_searching(user_id=call.from_user.id, is_searching=0, with_who=None)
    await call.message.delete()
    await call.message.answer('Main menu', reply_markup=main_menu.as_markup())


@router.callback_query(F.data == 'settings')
async def show_inline_menu(call: CallbackQuery):
    await call.message.edit_text('Settings', reply_markup=setting_kb.as_markup())


@router.callback_query(F.data == 'change_level')
async def show_inline_menu(call: CallbackQuery):
    await call.message.edit_text('Levels', reply_markup=reg_levels.as_markup())


@router.callback_query(F.data.startswith('change_to_'))
async def choose_level(call: CallbackQuery):
    selected_value = call.data.replace('change_to_', '')
    user_id = call.from_user.id
    await update_level(user_id, selected_value)
    await call.message.edit_text(f'Вы поменяли уровень владения на {selected_value}', reply_markup=only_back.as_markup())


@router.callback_query(F.data == 'change_about')
async def show_inline_menu(call: CallbackQuery):
    await call.message.edit_text('Write me your new bio', reply_markup=only_back.as_markup())


@router.callback_query(F.data == 'search')
async def choose_lvl(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выберите уровень владения языком собеседника:", reply_markup=reg_levels.as_markup())
    await state.set_state(MenuStatesGroup.level_reg)


async def notify_users(bot: Bot, user1_id: int, user2_id: int):
    profile1 = await get_profile(user1_id)
    profile2 = await get_profile(user2_id)

    if profile1 and profile2:
        level1, photo1, name1, age1, description1 = profile1
        level2, photo2, name2, age2, description2 = profile2

        # Notify user1
        await bot.send_photo(chat_id=user1_id,
                             photo=photo2,
                             caption=f"<b>{name2}</b>, {age2}\n{level2}\n<i>{description2}</i>",
                             parse_mode='HTML')

        # Notify user2
        await bot.send_photo(chat_id=user2_id,
                             photo=photo1,
                             caption=f"<b>{name1}</b>, {age1}\n{level1}\n<i>{description1}</i>",
                             parse_mode='HTML')

        # Notify both users to start chatting
        await bot.send_message(chat_id=user1_id, text="You can start chatting now!")
        await bot.send_message(chat_id=user2_id, text="You can start chatting now!")


@router.callback_query(StateFilter(MenuStatesGroup.level_reg))
async def searching(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    level = call.data  # Assuming the level is passed in the callback data

    text = "I'm searching"
    await call.message.edit_text(text=text, reply_markup=only_back.as_markup())
    await update_is_searching(user_id=user_id, is_searching=1, with_who=None)

    for i in range(1, 4):
        await asyncio.sleep(0.3)
        await call.message.edit_text(text=text + '.' * i, reply_markup=only_back.as_markup())

    found_match = False

    while not found_match:
        other_user = await is_someone_searching(level, user_id)
        if other_user:
            other_user_id = other_user[0]

            await call.message.delete()
            await call.message.answer(text="Match found! You can start chatting now.",
                                      reply_markup=skip_companion.as_markup(resize_keyboard=True))

            await notify_users(bot, user_id, other_user_id)
            await update_is_searching(user_id=user_id, is_searching=0, with_who=other_user_id)
            await update_is_searching(user_id=other_user_id, is_searching=0, with_who=user_id)
            print('They start!')
            found_match = True
        else:
            await asyncio.sleep(1)
