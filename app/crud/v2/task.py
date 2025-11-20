from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError,SQLAlchemyError

from app.models.task import Task
from app.schemas.schemas import TaskCreate,TaskRead
from app.utils.exceptions import DuplicateTaskError ,DatabaseError,TaskNotFoundError
from app.utils.logging import logger 

def create_task(db: Session, task: TaskCreate )->TaskRead:
    try:
        db_task = Task(**task.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    
    except IntegrityError as e:
        db.rollback() 
        logger.exception(f"Error creating task ",extra={"playload" : task.model_dump()})
        raise DuplicateTaskError("Task already exist")        
    except SQLAlchemyError as e :
        db.rollback()
        logger.exception(f"Error creating task ",extra={"playload" : task.model_dump()})
        raise DatabaseError("DB Error")

    
def get_tasks(db: Session)->list[TaskRead]:
    try:
        return db.query(Task).all()
    except SQLAlchemyError as e:
        logger.exception(f"Error getting tasks ")
        raise DatabaseError("DB Error")
    
    
def get_task_by_id(db: Session, task_id: int) -> TaskRead:
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise TaskNotFoundError("Task not found")
        return task
    except SQLAlchemyError as e:
        logger.exception(f"Error founding the task" , extra={"task_id" : task_id})
        raise DatabaseError("DB Error")    

def update_tasks(db: Session, task_id: int, task: TaskCreate) -> TaskRead:
    try:
        new_task = get_task_by_id(db, task_id)
        new_task.name = task.name
        new_task.description = task.description
        new_task.completed = task.completed
        db.commit()
        db.refresh(new_task)
        return new_task
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(f"DB Error updating task", extra={"task_id" : task_id,"playload" : task.model_dump() })
        raise DatabaseError("DB Error")


def delete_task(db: Session, task_id: int) -> dict:
    try:
        dl_task = get_task_by_id(db, task_id)
        db.delete(dl_task)
        db.commit()
        return {"Response": "OK"}
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(f"Error deleting task", extra={"task_id" : task_id })
        raise DatabaseError("DB Error deleting the task")
    

def get_tasks_by_name(db: Session, name: str) -> list[TaskRead]:
    try:
        tasks = db.query(Task).filter(Task.name.ilike(f"%{name}%")).all()
        return tasks
    except SQLAlchemyError as e:
        logger.exception(f"Error searching tasks by name")
        raise DatabaseError("DB Error")