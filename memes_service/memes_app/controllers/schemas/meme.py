from typing import Annotated
from uuid import UUID
import datetime as dt

from pydantic import BaseModel, Field


class MemeBase(BaseModel):
    title: Annotated[str, Field(min_length=3, max_length=100)]
    description: Annotated[str, Field(min_length=3, max_length=1000)]


class MemeRead(MemeBase):
    id: UUID
    created_at: dt.datetime
    image_url: str


class MemeCreate(MemeBase): ...


class MemeUpdate(MemeBase): ...
