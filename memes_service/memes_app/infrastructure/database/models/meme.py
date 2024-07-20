import datetime as dt

from sqlalchemy.orm import Mapped, mapped_column

from memes_app.infrastructure.database.models.base import BaseModel


class MemeModel(BaseModel):
    __tablename__ = 'meme'

    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    created_at: Mapped[dt.datetime] = mapped_column()
