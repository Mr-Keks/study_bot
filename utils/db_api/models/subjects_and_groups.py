from sqlalchemy import VARCHAR, INTEGER, Column, ForeignKey, sql

from utils.db_api.db_connect import TimedBaseModel


class Subjects_and_Groups(TimedBaseModel):
    __tablename__ = 'subjects_and_groups'

    id = Column(INTEGER, primary_key=True)
    subject_name = Column(VARCHAR(30), ForeignKey('subjects.subject_name'), nullable=False)
    group_key = Column(VARCHAR(16), ForeignKey('group_s.group_key'), nullable=False)
    subject_drive_folder = Column(VARCHAR(33), nullable=False)

    query: sql.Select



