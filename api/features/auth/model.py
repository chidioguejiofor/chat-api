from sqlalchemy import UniqueConstraint
from passlib.hash import pbkdf2_sha512
from settings import db
from api.base_classes import BaseModel


class User(BaseModel):
    username = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(320), nullable=False)
    password_hash = db.Column(db.String(), nullable=True)

    _password = None
    redirect_url = None
    __table_args__ = (
        UniqueConstraint(
            'username',
            name='unique_username'
        ),
        UniqueConstraint(
            'email',
            name='unique_email'
        ),
    )

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password_str):
        self._password = password_str
        self.password_hash = pbkdf2_sha512.hash(password_str)

    def verify_password(self, password_str):
        return pbkdf2_sha512.verify(password_str, self.password_hash)
