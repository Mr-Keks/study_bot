import pyperclip
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import FileIsTooBig
from keyboards.default import ready_kb, main_menu_, main_menu_action_button
from keyboards.inline.inline_subjects_buttons import list_subjects, main_menu, copy_button, list_groups
from loader import dp, bot
from states.states import add_subjects, add_home_work, get_home_work, group_key, group
from utils.db_api import commands
# from filters.group_filters.filters import IsGroup
from aiogram.types.input_file import InputFile

@dp.message_handler(commands=['main_menu'])
@dp.message_handler(text="Головне меню")
async def main_menu_mes(message: types.Message):
    await message.answer(f"Ви у головному меню", reply_markup=main_menu_action_button)


@dp.callback_query_handler(text='main_menu')
async def main_menu_call(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer(f"Ви у головному меню", reply_markup=main_menu_action_button)


# adding subjects
@dp.message_handler(commands=['add_subjects'])
@dp.message_handler(text="Додати предмети")
async def add_new_subjects(message: types.Message):
    await message.answer("Введіть назви предметів через кому:")
    await add_subjects.subjects.set()


@dp.message_handler(state=add_subjects.subjects)
async def adding_subjects(message: types.Message, state: FSMContext):
    # delete spaces
    #subjects = message.text.replace(" ", "").split(",")
    subjects = message.text.split(",")

    result = await commands.add_subjects(subjects, str(message.from_user.id))
    await message.answer(result, reply_markup=main_menu_)
    await state.finish()


# get subject
@dp.message_handler(commands=['chose_subject'])
@dp.message_handler(text="Додати домашнє")
async def chose_subject(message: types.Message):
    await message.answer("Виберіть предмет: ", reply_markup=await list_subjects(str(message.from_user.id)))
    await add_home_work.get_subject_name.set()


# from aiogram.dispatcher.filters import Text
# @dp.callback_query_handler(Text(startswith='select'))

# write home work
@dp.callback_query_handler(state=add_home_work.get_subject_name)
async def get_subject(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['subject'] = call.data

    await call.message.answer("Введіть домашнє:", reply_markup=ready_kb)
    await add_home_work.adding.set()


@dp.message_handler(content_types=['document', 'text'], state=add_home_work.adding)
async def adding_home_work_first(message: types.Message, state: FSMContext):
    try:
        if message.text == "Готово":
            data = await state.get_data()
            #list_data_values = list(data.values())

            subject_name = data.get("subject")
            text = data.get("text")
            file_name = data.get("files")
            file_path = data.get("mimeType")
            mime_type = data.get("files_path")

            if file_name is None:
                await commands.add_home_work(str(message.from_user.id), subject_name, text.split(', '))
            elif text is None:
                await commands.add_home_work_with_file(str(message.from_user.id),
                                                       subject_name,
                                                       "",
                                                       file_name.split(', '),
                                                       file_path.split(', '),
                                                       mime_type.split(', '))


            await state.finish()
            await message.answer("Домашнє успішно записане!")
        else:
            #data = await state.get_data()
            if message.text:
                async with state.proxy() as data:
                    if data.get('text') is None:
                        data['text'] = message.text
                    else:
                        data['text'] = data.get('text') + f', {message.text}'
            elif message.document:
                async with state.proxy() as data:
                    file = await bot.get_file(message.document.file_id)
                    # for first record
                    # можливо замінити поля в таблиці, записувати все в одне поле
                    if data.get('files') is None:
                        data['files'] = message.document.file_name
                        data['mimeType'] = message.document.mime_type
                        data['files_path'] = file.file_path

                    else:
                        data['files'] = data.get('files') + f', {message.document.file_name}'
                        data['mimeType'] = data.get('mimeType') + f', {message.document.mime_type}'
                        data['files_path'] = data.get('files_path') + f', {file.file_path}'
    except FileIsTooBig:
        document = message.document.file_id
        print(await bot.get_file(document))

# get home work
@dp.message_handler(text="Отримати домашнє")
async def get_home_work_func(message: types.Message):
    await message.answer("Виберіть предмет: ", reply_markup=await list_subjects(str(message.from_user.id)))
    await get_home_work.get_subject_name.set()


@dp.callback_query_handler(state=get_home_work.get_subject_name)
async def chose_subject_name(call: types.CallbackQuery, state: FSMContext):
    if call.data == "Назад":
        await call.message.edit_text("Повернутися назад:", reply_markup=main_menu)
        await state.finish()
    else:
        home_work = await commands.get_home_work(str(call.from_user.id), call.data)
        if home_work[0] is not None:
            await call.message.answer(home_work[0])
        if home_work[1] is not None:
            for file_name, file_content in home_work[1].items():
                await call.message.answer_document(InputFile(file_content, file_name))
    await main_menu_mes(call.message)


# get group_key
@dp.message_handler(text="Отримати код групи")
async def get_group_key(message: types.Message):
    await message.answer((await commands.get_user_and_group(str(message.from_user.id))).group_key,
                         reply_markup=copy_button)


@dp.callback_query_handler(text='copy')
async def copy_message(call: types.CallbackQuery):
    pyperclip.copy(call.message.text)
    await call.answer("Код успішно скопійовано")


# connect to group
@dp.message_handler(text="Підключитись до групи")
async def connect_to_group(message: types.Message):
    await message.answer("Введіть ключ групи:")
    await group_key.get_key.set()


@dp.message_handler(state=group_key.get_key)
async def connect_answer(message: types.Message, state: FSMContext):
    answer = await commands.connect_to_group(user_id=str(message.from_user.id), group_key=message.text)
    await message.answer(answer, reply_markup=main_menu_)
    await state.finish()


# change group
@dp.message_handler(text="Змінити групу")
async def change_group(message: types.Message):
    await message.answer("Виберіть групу", reply_markup=await list_groups(str(message.from_user.id)))
    await group.new_group.set()


@dp.callback_query_handler(state=group.new_group)
async def changing_group(call: types.CallbackQuery, state: FSMContext):
    answer = await commands.change_group_key(str(call.from_user.id), call.data)
    await call.message.answer(answer, reply_markup=main_menu_)
    await state.finish()
