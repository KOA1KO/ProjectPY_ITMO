from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, Bot, F
from aiogram.types import Message

from data.base import get_chatting_with_id, update_is_searching
from keyboards.inlinekb import only_back
from keyboards.keyboard import skip_companion
from translate import trans

router = Router()


@router.message(F.text == "Quit the conversation")
async def quit_conversation(message: Message, bot: Bot):
    user_id = message.from_user.id
    await message.answer("You've left the conversation\n___\n<tg-spoiler>Вы ушли из беседы</tg-spoiler>",
                         parse_mode="HTML", reply_markup=only_back.as_markup())
    companion_id = await get_chatting_with_id(user_id=user_id)
    await update_is_searching(user_id, 0, None)
    if companion_id:
        await bot.send_message(chat_id=companion_id, text="Your companion has decided to leave the "
                                                          "conversation.\n___\n<tg-spoiler>Ваш собеседник решил "
                                                          "покинуть беседу.</tg-spoiler>", parse_mode="HTML",
                               reply_markup=only_back.as_markup())
        await update_is_searching(companion_id, 0, None)


@router.message(F.text)
async def handle_chat(message: Message, bot: Bot):
    user_id = message.from_user.id
    companion_id = await get_chatting_with_id(user_id=user_id)
    if companion_id:
        text_plus_translation = trans(message.text)
        await bot.send_message(chat_id=companion_id, text=text_plus_translation, parse_mode="HTML",
                               reply_markup=skip_companion.as_markup(resize_keyboard=True))
