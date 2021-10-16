from sqlalchemy import VARCHAR, Column, sql

from utils.db_api.db_connect import TimedBaseModel

class Users(TimedBaseModel):
    __tablename__ = 'users'

    user_id = Column(VARCHAR(20), primary_key=True)

    query: sql.Select


