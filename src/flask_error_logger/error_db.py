from datetime import datetime

import bcrypt
from peewee import (Model,
                    BooleanField,
                    DateTimeField,
                    TextField,
                    CharField,
                    ForeignKeyField
                    )
from playhouse.pool import PooledSqliteDatabase
from playhouse.sqlite_ext import JSONField

from flask_error_logger.config import ERROR_DB

error_db = PooledSqliteDatabase(None)


class BaseModel(Model):
    created = DateTimeField(default=datetime.now)

    class Meta:
        database = error_db


class User(BaseModel):
    """Model for users
        role: ['admin', 'dev']
    """
    name = CharField()
    email = CharField(unique=True)
    role = CharField()
    password = CharField()

    @staticmethod
    def get_hashed_password(raw_pw: str) -> str:
        return bcrypt.hashpw(bytes(raw_pw, 'utf-8'), bcrypt.gensalt())

    @classmethod
    def create_user(cls, *args, **kwargs):
        """Create a new user instance"""
        if "name" not in kwargs:
            raise ValueError("You must provide a name")
        if "email" not in kwargs:
            raise ValueError("You must provide an email address")
        if "email" not in kwargs:
            raise ValueError("You must provide an email address")
        if "password" not in kwargs:
            raise ValueError("You must provide a password")
        hashed_password = cls.get_hashed_password(kwargs['password'])
        kwargs['password'] = hashed_password
        return cls.create(**kwargs)

    def set_password(self, raw_password: str):
        """save new password to the database"""
        self.password = self.get_hashed_password(raw_password)

    def check_password(self, plain_text_password: str) -> bool:
        return bcrypt.checkpw(bytes(plain_text_password, 'utf-8'), bytes(self.password, 'utf-8'))


class MailingList(BaseModel):
    name = CharField()
    shift_start = DateTimeField()
    shift_end = DateTimeField()


class MailingListUsers(BaseModel):
    mailing_list = ForeignKeyField(
        MailingList, backref="mailing_list", on_delete="CASCADE")
    user = ForeignKeyField(User, backref="mailing_list", on_delete="CASCADE")


class ErrorTable(BaseModel):
    uid = CharField(max_length=12)
    resolved_at = DateTimeField(null=True)
    resolved = BooleanField(default=False)
    resolved_by = CharField(null=True)
    url = CharField(max_length=400, null=True)
    method = CharField(max_length=10, null=True)
    context = JSONField()
    error_trace = TextField()
    comments = TextField(null=True)


def create_error_table():
    with error_db as db:
        db.create_tables(
            [User, MailingList, MailingListUsers, ErrorTable])
