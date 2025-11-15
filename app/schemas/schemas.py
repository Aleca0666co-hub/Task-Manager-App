from pydantic import BaseModel,Field

class TaskBase(BaseModel):
    name: str =Field(...,description="Name of the Task",min_length=3,max_length=50)

class TaskCreate(TaskBase):
    description: str = Field(..., max_length=500)
    completed: bool = False

class TaskRead(TaskBase):
    id: int
    description: str
    completed: bool

    model_config = {
        "from_attributes" : True
    }