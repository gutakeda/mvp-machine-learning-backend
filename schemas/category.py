from typing import List
from pydantic import BaseModel

class CategoryViewSchema(BaseModel):
    id: int
    name: str

class CategoriesListResponse(BaseModel):
    categories: List[CategoryViewSchema]