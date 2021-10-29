from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from utils.db_api.models import subjects_and_groups, users_and_groups
from utils.db_api import commands


async def list_subjects(user_id: str):
    all_subjects = types.InlineKeyboardMarkup(row_width=2)
    try:
        group_key = await commands.get_user_and_group(user_id)
        subjects = await commands.select_all_subjects(group_key.group_key)

        for subject in subjects:
            all_subjects.insert(InlineKeyboardButton(text=f"{subject.subject_name}", callback_data=subject))
        all_subjects.add(
            InlineKeyboardButton(text="Назад", callback_data='main_menu')
        )

        return all_subjects, subjects
    except AttributeError:
        return all_subjects.add(InlineKeyboardButton(text="Назад", callback_data='main_menu')), None


async def list_all_groups(user_id: str):
    all_groups = types.InlineKeyboardMarkup(row_width=2)
    try:
        groups = await commands.get_all_groups(user_id=user_id)

        for group in groups:
            g = InlineKeyboardButton(text=f"{group.group_name}", callback_data=f'{group.group_key}')
            all_groups.insert(g)

        all_groups.add(
            InlineKeyboardButton(text="Назад", callback_data='main_menu')
        )
        return all_groups

    except AttributeError:
        return None


async def list_groups(user_id: str):
    all_groups = types.InlineKeyboardMarkup(row_width=2)
    try:
        groups = await commands.get_groups(user_id=user_id)
        if len(groups):
            for group in groups:
                g = InlineKeyboardButton(text=f"{group.group_name}", callback_data=f'{group.group_key}')
                all_groups.insert(g)

            all_groups.add(
                InlineKeyboardButton(text="Назад", callback_data='main_menu')
            )
            return all_groups
        else:
            return groups
    except AttributeError:
        return None

back_button = types.InlineKeyboardMarkup()
back_button.insert(InlineKeyboardButton(text='Назад', callback_data='main_menu'))

main_menu_button = types.InlineKeyboardMarkup()
main_menu_button.insert(InlineKeyboardButton(text='Головне меню', callback_data='main_menu'))

copy_button = types.InlineKeyboardMarkup()
copy_button.insert(InlineKeyboardButton(text="Копіювати", callback_data='copy'))
copy_button.insert(InlineKeyboardButton(text='Головне меню', callback_data='main_menu'))
