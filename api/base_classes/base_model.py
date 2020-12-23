from settings import db
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declared_attr


def generate_current_time():
    return datetime.now(timezone.utc)


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    created_at = db.Column(db.DateTime(timezone=True),
                           default=generate_current_time)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__

    def save(self, commit=True):
        db.session.add(self)
        self._commit_or_flush(commit)

    def update(self):
        db.session.commit()

    @classmethod
    def _commit_or_flush(cls, commit):
        if commit:
            db.session.commit()
        else:
            db.session.flush()
