from app import dp, bot

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from data.base import edit_profile, get_profile, create_profile, isRegistered

from inlinekb import main_menu
from keyboards import get_kb, get_cancel_kb


class ProfileStatesGroup(StatesGroup):
    photo = State()
    name = State()
    age = State()
    description = State()


@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return

    await state.finish()
    await message.reply('Вы прервали создание анкеты!',
                        reply_markup=get_kb())


@dp.message_handler(commands=['reg'], state='*')
async def cmd_cancel(message: types.Message):
    user_id = message.from_user.id
    if await isRegistered(user_id):
        await message.answer(
            text="You are already registered!" + "\n___\n" +
                 '<tg-spoiler>Вы уже зарегистрированы!</tg-spoiler>',
            parse_mode='HTML'
        )
    else:
        await create_profile(user_id)
        await message.answer(
            text="Let's create your profile! To begin with, send me your photo. \n(It will be shown to everyone)" +
                 "\n___\n" + '<tg-spoiler>Давайте создадим ваш профиль! Для начала пришлите мне свою фотографию. (Она '
                             'будет показана всем)</tg-spoiler>', parse_mode='HTML', reply_markup=get_cancel_kb())
        await ProfileStatesGroup.photo.set()  # установили состояние фото


@dp.message_handler(commands=['edit_profile'], state='*')
async def cmd_cancel(message: types.Message):
    user_id = message.from_user.id
    await create_profile(user_id)
    await message.answer(
        text="Let's create edit your profile! Choose what do you want to change." +
             "\n___\n" + '<tg-spoiler>Давайте создадим ваш профиль! Для начала пришлите мне свою фотографию. (Она '
                         'будет показана всем)</tg-spoiler>', parse_mode='HTML', reply_markup=get_cancel_kb())
    await ProfileStatesGroup.photo.set()  # установили состояние фото


@dp.message_handler(lambda message: not message.photo, state=ProfileStatesGroup.photo)
async def check_photo(message: types.Message):
    await message.reply(text="That's not a photo." + "\n___\n" + '<tg-spoiler>Это не фото</tg-spoiler>',
                        parse_mode='HTML', reply_markup=get_cancel_kb())


@dp.message_handler(content_types=['photo'], state=ProfileStatesGroup.photo)
async def load_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await message.answer(text='Send me your first name (It will be shown to everyone)' + "\n___\n" +
                              '<tg-spoiler>Пришлите мне свое имя (оно будет показано всем)</tg-spoiler>',
                         parse_mode='HTML', reply_markup=get_cancel_kb())
    await ProfileStatesGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 100,
                    state=ProfileStatesGroup.age)
async def check_age(message: types.Message):
    await message.reply(text="That's not a real age!" + "\n___\n" + '<tg-spoiler>Это не фото</tg-spoiler>',
                        parse_mode='HTML', reply_markup=get_cancel_kb())


@dp.message_handler(state=ProfileStatesGroup.name)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer(
        text='How old are you? (Your age will be shown to everyone)' + "\n___\n" + '<tg-spoiler>Это не фото</tg-spoiler>',
        parse_mode='HTML', reply_markup=get_cancel_kb())
    await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.age)
async def load_age(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['age'] = message.text

    await message.answer(
        text='Tell me something about you (your hobbies or maybe phobias)' + "\n___\n" + '<tg-spoiler>Это не фото</tg-spoiler>',
        parse_mode='HTML', reply_markup=get_cancel_kb())
    await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.description)
async def load_desc(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['description'] = message.text
        data['user_id'] = message.from_user.id
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=data['photo'],
                             caption=f"<b>{data['name']}</b>, {data['age']}\n<i>{data['description']}</i>",
                             parse_mode='HTML')

    await edit_profile(state, user_id=message.from_user.id)
    await message.answer(text='Your profile is registered!' + "\n___\n" + '<tg-spoiler>Это не фото</tg-spoiler>',
                         parse_mode='HTML')
    await state.finish()


@dp.message_handler(commands=['profile'])
async def cmd_profile(message: types.Message):
    user_id = message.from_user.id
    profile = await get_profile(user_id)

    if profile:
        photo, name, age, description = profile
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=photo,
                             caption=f"<b>{name}</b>, {age}\n<i>{description}</i>",
                             parse_mode='HTML')
    else:
        await message.answer(
            text='Profile not found. Please register first.' + "\n___\n" + '<tg-spoiler>Профиль не найден. Пожалуйста, зарегистрируйтесь сначала.</tg-spoiler>',
            parse_mode='HTML')
