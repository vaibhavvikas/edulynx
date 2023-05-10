from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ChapterModel(BaseModel):
    chapter_no: int = Field(...)
    name: str = Field(...)
    text: str = Field(...)
    ratings_total: int = Field(...)
    ratings_count: int = Field(...)


class CourseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    date: str = Field(...)
    description: str = Field(...)
    domain: List[str] = Field(...)
    chapters: List[ChapterModel] = Field(...)
    ratings: float = Field(...)
    ratings_count: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
