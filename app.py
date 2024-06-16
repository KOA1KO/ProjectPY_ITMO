import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, Message

from keyboards.inlinekb import reg_menu, main_menu
from states import register, main, chatting

from config import BOT_TOKEN

from data.base import db_start, isRegistered

router = Router()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    print(user_id)
    if await isRegistered(user_id):
        await message.answer("Main menu", reply_markup=main_menu.as_markup())
    else:
        await message.answer(
            text='''Hi! Our bot is designed to keep your English proficiency up to date. You can use it to communicate '''
            '''with other people who speak English at your level and above. Let's register your profile! You can use the ''' 
            '''button "Register" to create your profile\n___\n<tg-spoiler>Привет! Наш бот создан для того, 
            чтобы поддерживать ваш уровень владения английским языком на должном уровне. С его помощью вы можете 
            общаться с другими людьми, владеющими английским на вашем уровне и выше. Давайте зарегистрируем ваш 
            профиль! Вы можете использовать кнопку "Регистрация", чтобы создать свой профиль.</tg-spoiler>''',
            parse_mode='HTML',
            reply_markup=reg_menu.as_markup())


async def start():
    await db_start()
    await bot.set_my_commands([
        BotCommand(command="start", description="Start the bot"),
    ])
    dp.include_router(router)
    dp.include_routers(register.router, main.router, chatting.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Start")
    asyncio.run(start())
