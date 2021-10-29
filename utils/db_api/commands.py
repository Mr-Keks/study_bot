import random
from typing import Optional

from asyncpg import UniqueViolationError, ForeignKeyViolationError
from sqlalchemy import and_

from .models.groups import Groups
from .models.users import Users
from .models.subjects import Subjects
from .models.subjects_and_groups import Subjects_and_Groups
from .models.home_works import Home_works
from .models.users_and_groups import Users_and_Groups

from data.config import key_values

from utils.db_api.drive.Drive import Drive

drive = Drive()


async def create_group(user_id: str, group_name: str):
    await turn_off_group_switcher(user_id=user_id)
    try:
        key_generate = ''.join(random.choice(key_values) for i in range(16))
        d = Drive()
        group_drive_folder = await drive.create_group_folder(group_name=group_name)
        group = Groups(group_key=key_generate, group_name=group_name, group_drive_folder=group_drive_folder)
        await group.create()
        if await Users.query.where(Users.user_id == user_id).gino.first():
            user = await Users.query.where(Users.user_id == user_id).gino.first()
        else:
            user = Users(user_id=user_id)
            await user.create()

        user_and_group = Users_and_Groups(user_id=user.user_id, group_key=group.group_key, group_switcher=True)
        await user_and_group.create()

        return "Група успішно створенна!"
    except UniqueViolationError:
        return "Упс.. шось післо не так(( \n" \
               "Спробуйте щераз!"


async def connect_to_group(user_id: str, group_key: str):
    if await get_group(group_key=group_key):
        check_user = await Users_and_Groups.query.where(Users_and_Groups.user_id == user_id).gino.first()
        if check_user is None:
            await Users(user_id=user_id).create()
        else:
            check_user_in_group = await Users_and_Groups.query.where(
                and_(
                    Users_and_Groups.user_id == user_id,
                    Users_and_Groups.group_key == group_key
                )
            ).gino.first()
            if check_user_in_group:
                return "Ви вже додані до цієї групи"
            await turn_off_group_switcher(user_id=user_id)
    else:
        return "Невірний ключ"
    await Users_and_Groups(user_id=user_id, group_key=group_key, group_switcher=True).create()
    return "Ви успішно додані до групи"


async def add_subjects(subjects: list, user_id: str):
    try:
        # зробити перевіртку на наявність передмету в таблиці, якщо він є то не додавати
        group = await get_user_and_group(user_id=user_id)
        group = await get_group(group_key=group.group_key)
        for subject in subjects:
            # verify for uniqueness
            if not await Subjects.query.where(Subjects.subject_name == subject).gino.first():
                await Subjects(subject_name=subject).create()

            subject_drive_folder_id = await drive.create_drive_folder(parent_folder=group.group_drive_folder,
                                                                      drive_folder_name=subject)

            await Subjects_and_Groups(subject_name=subject, group_key=group.group_key,
                                      subject_drive_folder=subject_drive_folder_id).create()
        return "Предмети успішно додані!"
    except UniqueViolationError:
        pass


async def add_home_work(user_id: str, subject_name: str, home_work_text: str, home_work_files: Optional[str],
                        files_mime: Optional[str], files_path: Optional[str]):
    try:
        group_and_user = await get_user_and_group(user_id)
        subject_and_group = await get_subject(group_and_user.group_key, subject_name)
        if home_work_files is not None:
            home_work_files_id = await drive.upload_home_work(home_work_files=home_work_files.split(", "),
                                                              files_mime=files_mime.split(", "),
                                                              drive_folder=subject_and_group.subject_drive_folder,
                                                              files_path=files_path.split(", "))
            if home_work_text is not None:
                home_work = Home_works(user_id=group_and_user.user_id, group_key=group_and_user.group_key,
                                       subject_name=subject_and_group.subject_name,
                                       home_work_text=home_work_text,
                                       home_work_files=home_work_files_id)
            else:
                home_work = Home_works(user_id=group_and_user.user_id, group_key=group_and_user.group_key,
                                       subject_name=subject_and_group.subject_name,
                                       home_work_files=home_work_files_id)
        else:
            home_work = Home_works(user_id=group_and_user.user_id, group_key=group_and_user.group_key,
                                   subject_name=subject_and_group.subject_name,
                                   home_work_text=home_work_text)
        await home_work.create()
    except AttributeError:
        return None


async def get_home_work(user_id: str, subject_name: str):
    group_and_user = await get_user_and_group(user_id=user_id)
    subject = await get_subject(group_key=group_and_user.group_key, subject_name=subject_name)
    home_work_data = await Home_works.query.where(
        and_(
            Home_works.user_and_group_id == group_and_user.id,
            Home_works.subjects_and_groups_id == subject.id)
    ).order_by(Home_works.id.desc()).gino.first()
    if home_work_data is None:
        return None
    home_work_date = home_work_data.updated_at.strftime("%m.%d.%Y")
    home_work_files = await drive.download_home_work_files(home_work_data.home_work_files)

    return [home_work_data.home_work_text, home_work_files, home_work_date]


async def select_all_subjects(group_key: str):
    subjects = await Subjects_and_Groups.query.where(Subjects_and_Groups.group_key == group_key).gino.all()
    return subjects


async def get_subject(group_key, subject_name):
    subject_group = await Subjects_and_Groups.query.where(
        (Subjects_and_Groups.group_key == group_key)).gino.all()
    s_and_g_id = ""
    for sub_name in subject_group:
        if sub_name.subject_name == subject_name:
            s_and_g_id = sub_name.id
            break
    subject = await Subjects_and_Groups.query.where(
        (Subjects_and_Groups.id == s_and_g_id)).gino.first()
    return subject


# має бути провірна на group_switcher
async def get_user_and_group(user_id: str):
    group = await Users_and_Groups.query.where(
        and_(
            Users_and_Groups.user_id == user_id,
            Users_and_Groups.group_switcher == True
        )
    ).gino.first()
    return group


async def get_group(group_key: str):
    try:
        return await Groups.query.where(
            Groups.group_key == group_key
        ).gino.first()
    except AttributeError:
        return None

async def turn_off_group_switcher(user_id: str):
    group = await get_user_and_group(user_id=user_id)
    if group:
        # change parameter 'group_switcher' for change group for current user
        await group.update(group_switcher=False).apply()


async def change_group_key(user_id: str, group_key: str):
    current_group = await get_user_and_group(user_id=user_id)
    new_group = await Users_and_Groups.query.where(
        and_(
            Users_and_Groups.user_id == user_id,
            Users_and_Groups.group_key == group_key
        )
    ).gino.first()
    await current_group.update(group_switcher=False).apply()
    await new_group.update(group_switcher=True).apply()
    return "Група успішно змінена"


async def get_groups(user_id: str):
    current_group = await get_user_and_group(user_id=user_id)
    if not current_group:
        raise AttributeError
    try:
        if not current_group:
            return None
        groups = await Users_and_Groups.query.where(Users_and_Groups.user_id == user_id).gino.all()
        group_list = []
        for group in groups:
            if group.group_key == current_group.group_key:
                continue
            group_list.append(await Groups.query.where(Groups.group_key == group.group_key).gino.first())
        return group_list
    except AttributeError:
        return None

async def get_all_groups(user_id: str):
    current_group = await get_user_and_group(user_id=user_id)
    if not current_group:
        raise AttributeError
    try:
        if not current_group:
            return None
        groups = await Users_and_Groups.query.where(Users_and_Groups.user_id == user_id).gino.all()
        group_list = []
        for group in groups:
            group_list.append(await Groups.query.where(Groups.group_key == group.group_key).gino.first())
        return group_list
    except AttributeError:
        return None


async def leave_user_group(user_id: str, group_key: str):
    try:
        await Users_and_Groups.delete.where(
            and_(
                Users_and_Groups.user_id == user_id,
                Users_and_Groups.group_key == group_key
            )
        ).gino.status()
        return "Ви успішно вийшли з групи"
    except Exception as ex:
        print(ex)
        return "Щось пішло не так..."
