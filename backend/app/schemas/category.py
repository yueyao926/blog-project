from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    parent_id: int | None = None


class CategoryOut(BaseModel):
    id: int
    name: str
    parent_id: int | None = None

    class Config:
        from_attributes = True
