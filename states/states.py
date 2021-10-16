from aiogram.dispatcher.filters.state import StatesGroup, State


class create_group(StatesGroup):
    create = State()
    # finish = State()


class connect_to_db(StatesGroup):
    connect = State()
    finish = State()


class add_subjects(StatesGroup):
    subjects = State()
    # finish = State()


class add_home_work(StatesGroup):
    get_subject_name = State()
    adding = State()
    adding_second = State()
    saving = State()


class get_home_work(StatesGroup):
    get_subject_name = State()


class group_key(StatesGroup):
    get_key = State()

class group(StatesGroup):
    new_group = State()



