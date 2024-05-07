from pydantic import BaseModel


class BasicDevice(BaseModel):
    id: int
    serial: str
    name: str
