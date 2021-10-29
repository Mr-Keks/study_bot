from sqlalchemy import VARCHAR, INTEGER, Column, ForeignKey, ARRAY
from sqlalchemy import sql
from utils.db_api.db_connect import TimedBaseModel


class Home_works(TimedBaseModel):
    __tablename__ = 'home_works'

    id = Column(INTEGER, primary_key=True)
    user_id = Column(ForeignKey("users.user_id"), nullable=False)
    group_key = Column(ForeignKey("group_s.group_key"), nullable=False)
    subject_name = Column(VARCHAR(30), ForeignKey('subjects.subject_name'), nullable=False)
    home_work_text = Column(VARCHAR(255), nullable=True)
    home_work_files = Column(ARRAY(VARCHAR), nullable=True)

    query: sql.Select
