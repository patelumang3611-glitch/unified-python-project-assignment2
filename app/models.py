from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int

class Reader(BaseModel):
    id: int
    name: str
    membership_id: str

class Staff(BaseModel):
    id: int
    name: str
    position: str
