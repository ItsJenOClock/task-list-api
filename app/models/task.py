from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]]

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=bool(self.completed_at)
        )

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],
            description=task_data["description"]
        )
