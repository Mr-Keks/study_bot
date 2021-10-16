from sqlalchemy import VARCHAR, Integer, Column, sql

from utils.db_api.db_connect import TimedBaseModel


class Groups(TimedBaseModel):
    __tablename__ = 'group_s'

    group_key = Column(VARCHAR(16), primary_key=True)
    group_name = Column(VARCHAR(20), nullable=False)
    group_drive_folder = Column(VARCHAR(33), nullable=False)

    query: sql.Select



