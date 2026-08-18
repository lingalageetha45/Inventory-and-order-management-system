from pydantic import BaseModel, ConfigDict

from app.enums.enums import CategoryStatus


class CategoryCreate(BaseModel):
    name: str
    description: str | None = None
    status: CategoryStatus = CategoryStatus.ACTIVE


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: CategoryStatus | None = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None
    status: CategoryStatus

    model_config = ConfigDict(from_attributes=True)