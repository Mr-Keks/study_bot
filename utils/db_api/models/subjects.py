from sqlalchemy import VARCHAR, INTEGER, Column
from sqlalchemy import sql

from utils.db_api.db_connect import TimedBaseModel

class Subjects(TimedBaseModel):
    __tablename__ = 'subjects'

    subject_name = Column(VARCHAR(50), primary_key=True)

    query: sql.Select





