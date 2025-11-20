from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError,SQLAlchemyError

from app.models.task import Task
from app.schemas.schemas import TaskCreate,TaskRead
from app.utils.exceptions import DuplicateTaskError ,DatabaseError,TaskNotFoundError
from app.utils.logging import logger 



def create_task(db: Session, task: TaskCreate ):
    try:
        db_task = Task(**task.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    
    except IntegrityError as e:
        db.rollback() 
        logger.exception(f"Error creating task: {e.orig}",exc_info={"playload":task.model_dump()})
        raise DuplicateTaskError("Task already exist")        
    except SQLAlchemyError as e :
        db.rollback()
        logger.exception(f"DB Error:{e} ")
        raise DatabaseError("DB Error")

def get_tasks(db: Session):
    try:
        return db.query(Task).all()
    except SQLAlchemyError as e:
        db.rollback()
        logger.critical(f"Error getting task:{e}")
        raise RuntimeError("DB Error")
    
    
#-----------------------------New implements to prove-------------------
def  update_tasks(db:Session,task_id:int ,task:TaskCreate )->TaskRead:
    try:
        new_task = db.query(Task).filter(Task.id==task_id).first()
        if not new_task:
            raise TaskNotFoundError("Task not found")
        
        if new_task:
            new_task.name=task.name
            new_task.description=task.description
            new_task.completed=task.completed
        db.commit()
        db.refresh(new_task)
        return new_task
    except SQLAlchemyError as e :
        db.rollback()
        logger.error(f"DB Error:{e}")
        raise DatabaseError("DB Error")



def delete_task(db:Session,task_id:int)->dict:
    try:
        dl_task=db.query(Task).filter(Task.id==task_id).first()
        if not dl_task:
            raise TaskNotFoundError("Task not found")
        db.delete(dl_task)
        db.commit()
        return {"Response" :'OK'}
    except SQLAlchemyError as e :
        db.rollback
        logger.error(f"Error deleting task :{e}")
        raise DatabaseError("DB Error")
    
