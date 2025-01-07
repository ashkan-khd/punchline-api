from typing import List

from app import db
from datetime import datetime


class JokeValueFields:
    id: str
    value: str
    categories: List[str]
    created_at: datetime
    updated_at: datetime
    source: str


class Joke(db.Model, JokeValueFields):
    __tablename__ = 'jokes'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Text, nullable=False)
    categories = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)

    @property
    def source(self) -> str:
        return "local"

    def to_dict(self):
        return {
            'id': self.id,
            'value': self.value,
            'categories': self.categories,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
