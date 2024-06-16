from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram import Router, F, Bot

from data.base import search_inData
from keyboards.inlinekb import main_menu, setting_kb, reg_levels, only_back, choose_activate_kb

router = Router()


class MenuStatesGroup(StatesGroup):
    level_reg = State()
    search = State()


@router.callback_query(F.data == 'main')
async def delete_msg(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer('Main menu', reply_markup=main_menu.as_markup())


@router.callback_query(F.data == 'settings')
async def show_inline_menu(call: CallbackQuery):
    await call.message.edit_text('Settings', reply_markup=setting_kb.as_markup())


@router.callback_query(F.data == 'change_level')
async def show_inline_menu(call: CallbackQuery):
    await call.message.edit_text('Levels', reply_markup=reg_levels.as_markup())


@router.callback_query(F.data == 'change_about')
async def show_inline_menu(call: CallbackQuery):
    await call.message.edit_text('Write me your new bio', reply_markup=only_back.as_markup())


@router.callback_query(F.data == 'search')
async def choose_lvl(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выберите уровень владения языком собеседника:", reply_markup=reg_levels.as_markup())
    await state.set_state(MenuStatesGroup.level_reg)


@router.callback_query(StateFilter(MenuStatesGroup.level_reg))
async def searching(call: CallbackQuery, state: FSMContext, bot: Bot):
    level = call.data
    index = 0

    profile = await search_inData(level, index)

    if profile:
        choose_keys = choose_activate_kb(index)
        await bot.send_photo(chat_id=call.from_user.id,
                             photo=profile['photo'],
                             caption=f"<b>{profile['name']}</b>, {profile['age']}\n{profile['level']}\n<i>{profile['description']}</i>",
                             parse_mode='HTML',
                             reply_markup=choose_keys.as_markup())

        await state.update_data(profile_index=index, profile_level=level)
        await state.set_state(MenuStatesGroup.search)  # Set the state to search for navigation
    else:
        await bot.send_message(chat_id=call.from_user.id, text="No profile found for the given level.")


@router.callback_query(StateFilter(MenuStatesGroup.search))
async def navigate_profile(call: CallbackQuery, state: FSMContext, bot: Bot, direction: int):
    data = await state.get_data()
    level = data.get('profile_level')
    index = data.get('profile_index', 0) + direction

    profile = await search_inData(level, index)

    if profile:
        # Check if the profile's user ID is not the same as the caller's user ID
        if int(profile['user_id']) != int(call.from_user.id):
            choose_keys = choose_activate_kb(index)
            await bot.edit_message_media(media=InputMediaPhoto(profile['photo'],
                                                               caption=f"<b>{profile['name']}</b>, {profile['age']}\n{profile['level']}\n<i>{profile['description']}</i>"),
                                         chat_id=call.from_user.id,
                                         message_id=call.message.message_id,
                                         reply_markup=choose_keys.as_markup())

            await state.update_data(profile_index=index)
        else:
            # Update the state to skip the current user's profile
            await state.update_data(profile_index=index)
            await navigate_profile(call, state, bot, direction)
    else:
        await bot.answer_callback_query(call.id, "No more profiles available.")


@router.callback_query(F.data.startswith('next_'))
async def next_profile(call: CallbackQuery, state: FSMContext, bot: Bot):
    await navigate_profile(call, state, bot, direction=1)


@router.callback_query(F.data.startswith('prev_'))
async def prev_profile(call: CallbackQuery, state: FSMContext, bot: Bot):
    await navigate_profile(call, state, bot, direction=-1)