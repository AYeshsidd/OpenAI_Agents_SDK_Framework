from pydantic import BaseModel

class Data_schema(BaseModel):
    is_cricket_query: bool
    salary_related_query: bool
    Expert_opinion: str


