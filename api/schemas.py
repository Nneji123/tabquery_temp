from pydantic import BaseModel


class Question(BaseModel):
    quest: str
