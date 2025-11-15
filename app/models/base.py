from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class BaseTask(Base):
    __tablename__ = "base_tasks"
    id = Column(Integer, primary_key=True ,index=True)
    name = Column(String, nullable=False)
    type=Column(String)
    
    __mapper_args__ = {
        "polymorphic_identity": "base_task",
        "polymorphic_on": type
    }