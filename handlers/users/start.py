from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import create_or_connect, ready_kb, main_menu_or_add_subjects
from loader import dp, bot
from states.states import create_group
from utils.db_api import commands


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer("Виберіть дію:", reply_markup=create_or_connect)


@dp.message_handler(lambda message: message.text == "Створити групу")
async def create_group_(message: types.Message):
    await message.answer("Введіть назву групи:")
    await create_group.create.set()


@dp.message_handler(state=create_group.create)
async def set_group_name_and_save(message: types.Message,  state: FSMContext):
    group_name = message.text
    result = await commands.create_group(str(message.from_user.id), group_name)
    await message.answer(result, reply_markup=main_menu_or_add_subjects)
    await state.finish()






