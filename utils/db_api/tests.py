import asyncio

from data import config
from utils.db_api import commands
from utils.db_api.db_connect import db


async def test():
    print("connecting")
    await db.set_bind(config.POSTGRES_URI)
    await db.gino.drop_all()
    await db.gino.create_all()
    #s = await commands.get_subject("SKDjskIqLp2quhdJ", "asd")
    #print(s.subject_name)
    # print("Create groups")
    # subject = await commands.select_all_subjects("9bzlAl13RmoTNwfE")
    # print(f"{subject[0].subject_name}")
    # for s in subject:
    #   print(s.subject_name)
    # await commands.create_group("1.1", "pf")
    # await commands.add_subjects(["ukr", "mat"], "1")


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
