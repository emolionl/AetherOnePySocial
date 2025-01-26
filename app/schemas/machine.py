from pydantic import BaseModel

class MachineCreate(BaseModel):
    machine_name: str
    description: str
    api_key: str

class MachineResponse(BaseModel):
    id: int
    machine_name: str
    description: str
    api_key: str

    class Config:
        orm_mode = True