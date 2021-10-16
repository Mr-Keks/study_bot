from sqlalchemy import ForeignKey, BOOLEAN, INTEGER, Column, sql
from utils.db_api.db_connect import TimedBaseModel


class Users_and_Groups(TimedBaseModel):
    __tablename__ = 'users_and_groups'

    id = Column(INTEGER, primary_key=True)
    user_id = Column(ForeignKey("users.user_id"), nullable=False)
    group_key = Column(ForeignKey("group_s.group_key"), nullable=False)
    group_switcher = Column(BOOLEAN, nullable=False)

    query: sql.Select
