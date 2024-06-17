from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup

from data.base import edit_profile, get_profile, create_profile, isRegistered
from keyboards.inlinekb import main_menu, reg_menu, levels, to_menu
from keyboards.keyboard import cancel_kb

router = Router()


class ProfileStatesGroup(StatesGroup):
    level = State()
    photo = State()
    name = State()
    age = State()
    description = State()


@router.message(Command("cancel"), StateFilter(ProfileStatesGroup()))
async def cmd_cancel(message: Message, state: FSMContext):
    if state is None:
        return

    await state.clear()
    await message.reply('Вы прервали создание анкеты!',
                        reply_markup=reg_menu.as_markup())


@router.callback_query(F.data == 'register', StateFilter(None))
async def show_inline_menu(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if await isRegistered(user_id):
        await call.message.answer("You are already registered!" + "\n___\n" +
                                  '<tg-spoiler>Вы уже зарегистрированы!</tg-spoiler>', parse_mode='HTML',
                                  reply_markup=main_menu.as_markup(resize_keyboard=True))
    else:
        await call.message.answer(
            text="Let's create your profile! First, choose your level of English.\n" +
                 "\n___\n" + '<tg-spoiler>Давайте создадим ваш профиль! Для начала выберите свой уровень знания '
                             'английского языка.</tg-spoiler>',
            parse_mode='HTML', reply_markup=levels.as_markup())
        await state.set_state(ProfileStatesGroup.level)


@router.callback_query(StateFilter(ProfileStatesGroup.level))
async def show_inline_menu(call: CallbackQuery, state: FSMContext):
    await state.update_data(level=call.data)
    await call.message.answer(text="To begin with, send me a picture of yourself. \n(It will be shown to everyone)" +
                                   "\n___\n" + '<tg-spoiler>Для начала пришлите мне свою фотографию. \n(Она будет '
                                               'показана всем)</tg-spoiler>',
                              parse_mode='HTML', reply_markup=cancel_kb.as_markup(resize_keyboard=True))
    await state.set_state(ProfileStatesGroup.photo)


@router.message(lambda message: not message.photo, StateFilter(ProfileStatesGroup.photo))
async def check_photo(message: Message):
    await message.reply(text="That's not a photo." + "\n___\n" + '<tg-spoiler>Это не фото</tg-spoiler>',
                        parse_mode='HTML', reply_markup=cancel_kb.as_markup(resize_keyboard=True))


@router.message(lambda message: message.photo, StateFilter(ProfileStatesGroup.photo))
async def load_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[0].file_id)
    await message.answer(text='Send me your first name (It will be shown to everyone)' + "\n___\n" +
                              '<tg-spoiler>Пришлите мне свое имя (оно будет показано всем)</tg-spoiler>',
                         parse_mode='HTML', reply_markup=cancel_kb.as_markup(resize_keyboard=True))
    await state.set_state(ProfileStatesGroup.name)


@router.message(lambda message: not message.text.isdigit() or float(message.text) > 100,
                StateFilter(ProfileStatesGroup.age))
async def check_age(message: Message):
    await message.reply(
        text="That's not a real age!" + "\n___\n" + '<tg-spoiler>Это не настоящий возраст!</tg-spoiler>',
        parse_mode='HTML', reply_markup=cancel_kb.as_markup(resize_keyboard=True))


@router.message(StateFilter(ProfileStatesGroup.name))
async def load_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text='How old are you? (Your age will be shown to everyone)' + "\n___\n" + '<tg-spoiler>Сколько вам лет? (Ваш '
                                                                                   'возраст будет показан '
                                                                                   'всем)</tg-spoiler>',
        parse_mode='HTML', reply_markup=cancel_kb.as_markup(resize_keyboard=True))
    await state.set_state(ProfileStatesGroup.age)


@router.message(StateFilter(ProfileStatesGroup.age))
async def load_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer(
        text='Tell me something about yourself (your hobbies or maybe phobias).' + "\n___\n" + '<tg-spoiler'
                                                                                               '>Расскажите мне'
                                                                                               'что-нибудь о себе (твои '
                                                                                               'хобби или, может быть, '
                                                                                               'фобии).</tg-spoiler>',
        parse_mode='HTML', reply_markup=cancel_kb.as_markup(resize_keyboard=True))
    await state.set_state(ProfileStatesGroup.description)


@router.message(StateFilter(ProfileStatesGroup.description))
async def load_desc(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    await state.update_data(description=message.text)
    await create_profile(user_id)
    data = await state.get_data()
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=data['photo'],
                         caption=f"<b>{data['name']}</b>, {data['age']}\n{data['level']}\n<i>{data['description']}</i>",
                         parse_mode='HTML')

    await edit_profile(state, user_id=message.from_user.id)
    await state.clear()
    await message.answer(
        text='Your profile is registered!' + "\n___\n" + '<tg-spoiler>Ваш профиль зарегистрирован!</tg-spoiler>',
        parse_mode='HTML', reply_markup=to_menu.as_markup())


@router.callback_query(F.data == 'profile')
async def cmd_profile(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    profile = await get_profile(user_id)
    if profile:
        await call.message.delete()
        level, photo, name, age, description = profile
        await bot.send_photo(chat_id=call.from_user.id,
                             photo=photo,
                             caption=f"<b>{name}</b>, {age}\n{level}\n<i>{description}</i>",
                             parse_mode='HTML', reply_markup=to_menu.as_markup())
    else:
        await call.message.answer(
            text='Profile not found. Please register first.' + "\n___\n" + '<tg-spoiler>Профиль не найден. '
                                                                           'Пожалуйста, зарегистрируйтесь '
                                                                           'сначала.</tg-spoiler>',
            parse_mode='HTML', reply_markup=to_menu.as_markup())
