from sqlalchemy import Column, String, Boolean ,Integer ,ForeignKey
from .base import BaseTask

class Task(BaseTask):
    __tablename__ = "tasks"
    id = Column(Integer, ForeignKey("base_tasks.id"),primary_key=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
    
    __mapper_args__ = {
        "polymorphic_identity": "task"
    }
    
    