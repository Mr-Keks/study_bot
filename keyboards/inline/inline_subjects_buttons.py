from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from utils.db_api.models import subjects_and_groups, users_and_groups
from utils.db_api import commands


async def list_subjects(user_id: str):
    all_subjects = types.InlineKeyboardMarkup(row_width=2)
    group_key = await commands.get_user_and_group(user_id)
    subjects = await commands.select_all_subjects(group_key.group_key)

    for subject in subjects:
        s = InlineKeyboardButton(text=f"{subject.subject_name}", callback_data=f'{subject.subject_name}')
        all_subjects.insert(s)

    all_subjects.add(
        InlineKeyboardButton(text="Назад", callback_data=f'Назад')
    )
    return all_subjects


async def list_groups(user_id: str):
    all_groups = types.InlineKeyboardMarkup(row_width=2)
    groups = await commands.get_groups(user_id=user_id)

    for group in groups:
        g = InlineKeyboardButton(text=f"{group.group_name}", callback_data=f'{group.group_key}')
        all_groups.insert(g)

    all_groups.add(
        InlineKeyboardButton(text="Назад", callback_data=f'Назад')
    )
    return all_groups


main_menu = types.InlineKeyboardMarkup()
main_menu.insert(InlineKeyboardButton(text='Головне меню', callback_data='main_menu'))

copy_button = types.InlineKeyboardMarkup()
copy_button.insert(InlineKeyboardButton(text="Копіювати", callback_data='copy'))
copy_button.insert(InlineKeyboardButton(text='Головне меню', callback_data='main_menu'))
