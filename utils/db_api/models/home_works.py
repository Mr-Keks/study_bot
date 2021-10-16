from sqlalchemy import VARCHAR, INTEGER, Column, ForeignKey, ARRAY
from sqlalchemy import sql
from utils.db_api.db_connect import TimedBaseModel


class Home_works(TimedBaseModel):
    __tablename__ = 'home_works'

    id = Column(INTEGER, primary_key=True)
    user_and_group_id = Column(INTEGER, ForeignKey('users_and_groups.id'), nullable=False)
    subjects_and_groups_id = Column(INTEGER, ForeignKey('subjects_and_groups.id'), nullable=False)
    home_work_text = Column(VARCHAR(255), nullable=True)
    home_work_files = Column(ARRAY(VARCHAR), nullable=True)

    query: sql.Select
