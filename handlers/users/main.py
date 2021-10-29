import pyperclip
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default import ready_kb, main_menu_, main_menu_action_button, create_or_connect, add_subjects_button
from keyboards.inline.inline_subjects_buttons import list_subjects, back_button, copy_button, list_groups, \
     list_all_groups, main_menu_button
from loader import dp, bot
from states.states import add_subjects, add_home_work, get_home_work, group_key, group, group_leave
from utils.db_api import commands
from aiogram.types.input_file import InputFile


@dp.message_handler(commands=['main_menu'])
@dp.message_handler(text="Головне меню")
async def main_menu_mes(message: types.Message):
    await message.answer(f"Ви у головному меню", reply_markup=main_menu_action_button)


@dp.callback_query_handler(text=['main_menu'])
async def main_menu_call(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer("Ви у головному меню", reply_markup=main_menu_action_button)


# adding subjects
@dp.message_handler(commands=['add_subjects'])
@dp.message_handler(text="Додати предмети")
async def add_new_subjects(message: types.Message):
    await message.answer("Введіть назви предметів через кому:")
    await add_subjects.subjects.set()


@dp.callback_query_handler(text=['add_subjects'])
async def add_new_subjects_call(call: types.CallbackQuery):
    await call.message.answer("Введіть назви предметів через кому:")
    await add_subjects_button.subjects.set()


@dp.message_handler(state=add_subjects.subjects)
async def adding_subjects(message: types.Message, state: FSMContext):
    # delete spaces
    # subjects = message.text.replace(" ", "").split(",")
    subjects = message.text.split(",")

    result = await commands.add_subjects(subjects, str(message.from_user.id))
    await message.answer(result, reply_markup=main_menu_)
    await state.finish()


# get subject
@dp.message_handler(commands=['chose_subject'])
@dp.message_handler(text="Додати домашнє")
async def chose_subject(message: types.Message):
    subjects_keyboard, len_subjects_bool = await list_subjects(str(message.from_user.id))
    if len_subjects_bool is None:
        await message.answer("Ви не додані до жодної групи!\n"
                             "Створіть, або підключіться до існуючої ", reply_markup=create_or_connect)
        await message.answer("Повернутися в головне меню", reply_markup=subjects_keyboard)

    elif not len_subjects_bool:
        await message.answer("У вас ще не додані предмети: ", reply_markup=add_subjects_button)
        await message.answer("Повернутись в головне меню", reply_markup=subjects_keyboard)

    else:
        await message.answer("Виберіть предмет: ", reply_markup=subjects_keyboard)
        await add_home_work.get_subject_name.set()


# from aiogram.dispatcher.filters import Text
# @dp.callback_query_handler(Text(startswith='select'))

# add home work
@dp.callback_query_handler(state=add_home_work.get_subject_name)
async def get_subject(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'main_menu':
        await main_menu_call(call, state)
    else:
        async with state.proxy() as data:
            data['subject'] = call.data
        await call.message.answer("Введіть домашнє:", reply_markup=ready_kb)
        await add_home_work.adding.set()


@dp.message_handler(content_types=['document', 'text', 'photo', 'voice', 'audio'], state=add_home_work.adding)
async def adding_home_work_first(message: types.Message, state: FSMContext):
    if message.text == "Готово":
        data = await state.get_data()
        # list_data_values = list(data.values())

        subject_name = data.get("subject")
        text = data.get("text")
        file_name = data.get("files")
        file_path = data.get("mimeType")
        mime_type = data.get("files_path")

        await commands.add_home_work(str(message.from_user.id), subject_name, text, file_name, file_path, mime_type)
        await state.finish()
        await message.answer("Домашнє успішно записане!")
        await main_menu_mes(message)

    else:
        # data = await state.get_data()
        if message.text:
            print('text')
            async with state.proxy() as data:
                if data.get('text') is None:
                    data['text'] = message.text
                else:
                    data['text'] = data.get('text') + f', {message.text}'
        elif message.document:
            await getting_file(message.document, state)
        elif message.photo:
            await getting_file(message.photo[-1], state)
        elif message.audio:
            await getting_file(message.audio, state)
        elif message.voice:
            await getting_file(message.voice, state)
        else:
            await message.answer("Даний тим не підтримується!")


async def getting_file(file_mes, state):
    async with state.proxy() as data:
        file = await bot.get_file(file_mes.file_id)
        file_types = {"Voice": '.ogg', 'PhotoSize': '.jpg'}
        photo_mime = 'image/jpeg'

        if data.get('files') is None:
            try:
                data['files'] = file_mes.file_name
            except AttributeError:
                # for voice message and photo
                data['files'] = file_mes.file_unique_id + file_types.get(type(file_mes).__name__)
            try:
                data['mimeType'] = file_mes.mime_type
            except AttributeError:
                data['mimeType'] = photo_mime
            data['files_path'] = file.file_path

        else:
            try:
                data['files'] = data.get('files') + f', {file_mes.file_name}'
            except AttributeError:
                # for voice message and photo
                data['files'] = data.get(
                    'files') + f', {file_mes.file_unique_id + file_types.get(type(file_mes).__name__)} '
            try:
                data['mimeType'] = data.get('mimeType') + f', {file_mes.mime_type}'
            except AttributeError:
                data['mimeType'] = data.get('mimeType') + f', {photo_mime}'
            data['files_path'] = data.get('files_path') + f', {file.file_path}'


# get home work
@dp.message_handler(text="Отримати домашнє")
async def get_home_work_func(message: types.Message):
    subjects_keyboard, len_subjects_bool = await list_subjects(str(message.from_user.id))
    if not len_subjects_bool:
        await message.answer("У вас ще не додані предмети: ", reply_markup=add_subjects_button)
        await message.answer("Повернутись в головне меню", reply_markup=back_button)
    else:
        await message.answer("Виберіть предмет: ", reply_markup=subjects_keyboard)
        await get_home_work.get_subject_name.set()


@dp.callback_query_handler(state=get_home_work.get_subject_name)
async def chose_subject_name(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'main_menu':
        await main_menu_call(call, state)
    else:
        home_work = await commands.get_home_work(str(call.from_user.id), call.data)
        if home_work is None:
            await call.message.answer("Домашнє ще не записане на цей предмет")
        else:
            await call.message.answer(f"дата запису домашнього: {home_work[2]}")

            if home_work[0] is not None:
                await call.message.answer(home_work[0])

            if home_work[1] is not None:
                for file_name, file_content in home_work[1].items():
                    await call.message.answer_document(InputFile(file_content, file_name))
        await state.finish()
        await main_menu_mes(call.message)


# get group_key
@dp.message_handler(text="Отримати код групи")
async def get_group_key(message: types.Message):
    key = await commands.get_user_and_group(str(message.from_user.id))
    if key:
        await message.answer(key.group_key, reply_markup=copy_button)
    else:
        await message.answer("Ви не додані до жодної групи!\n"
                             "Створіть, або підключіться до існуючої ", reply_markup=create_or_connect)
        await message.answer("Повернутися в головне меню", reply_markup=back_button)


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
    group_list = await list_groups(str(message.from_user.id))

    if group_list is None:
        await message.answer("Ви не додані до жодної групи!\n"
                             "Створіть, або підключіться до існуючої ", reply_markup=create_or_connect)
        await message.answer("Повернутися в головне меню", reply_markup=back_button)
    elif len(group_list) == 0:
        await message.answer("Ви додані лише до однієї групи!")
        await message.answer("Повернутися в головне меню", reply_markup=back_button)
    else:
        await message.answer("Виберіть групу", reply_markup=group_list)
        await group.new_group.set()


@dp.callback_query_handler(state=group.new_group)
async def changing_group(call: types.CallbackQuery, state: FSMContext):
    if call.data != 'main_menu':
        answer = await commands.change_group_key(str(call.from_user.id), call.data)
        await call.message.answer(answer, reply_markup=main_menu_)
        await state.finish()
    else:
        await main_menu_mes(call.message)


# leave a group
@dp.message_handler(text="Вийти з групи")
async def leave_group_get_group(message: types.Message):
    group_list = await list_all_groups(str(message.from_user.id))

    if group_list:
        await message.answer("Виберіть групу", reply_markup=group_list)
        await group_leave.leave.set()
    else:
        await message.answer("Ви не додані до жодної групи!\n"
                             "Створіть, або підключіться до існуючої ", reply_markup=create_or_connect)
        await message.answer("Повернутися в головне меню", reply_markup=back_button)


@dp.callback_query_handler(state=group_leave.leave)
async def leave_group(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'main_menu':
        await main_menu_call(call, state)
    else:
        result = await commands.leave_user_group(str(call.from_user.id), call.data)
        await state.finish()
        await call.answer(result)
        await call.message.answer("Повернутись в головне меню", reply_markup=main_menu_button)