from aiogram import executor, Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN

from keyboards import get_kb

from data.base import db_start


async def on_startup(_):
    await db_start()


storage = MemoryStorage()
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot,
                storage=storage)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.answer(text="Hi! Our bot is designed to keep your English proficiency up to date. You can use it to "
                              "communicate with other people who speak English at your level and above. Let's "
                              "register your profile! You can use the command /reg to create your profile" + "\n___\n" +
                              '<tg-spoiler>Привет! Наш бот создан для того, чтобы поддерживать ваш уровень владения '
                              'английским языком на должном уровне. С его помощью вы можете общаться с другими '
                              'людьми, владеющими английским на вашем уровне и выше. Давайте зарегистрируем ваш '
                              'профиль! Ты можешь воспользоваться командой /reg чтобы создать свой '
                              'профиль.</tg-spoiler>',
                         parse_mode='HTML',
                         reply_markup=get_kb())


if __name__ == '__main__':
    from states import dp

    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
