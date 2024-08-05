import datetime
import uuid

from typing import Type
from config import PG_DSN

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import (Integer, String, Float, UUID, DateTime, func, ForeignKey, Table, Column, CheckConstraint,
                        Boolean, UniqueConstraint)

from extra_types import ModelName

engine = create_async_engine(
    PG_DSN
)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


role_rights = Table(
    "role_right_relation",
    Base.metadata,
    Column("role_id", ForeignKey("role.id"), index=True),
    Column("right_id", ForeignKey("right.id"), index=True),
)
user_roles = Table(
    "user_role_relation",
    Base.metadata,
    Column("user_id", ForeignKey("user.user_id"), index=True),
    Column("role_id", ForeignKey("role.id"), index=True),
)


class Right(Base):
    __tablename__ = "right"
    __table_args__ = (CheckConstraint("model in ('user', 'advertisement','right','role')"),
                      UniqueConstraint("model", "write", "read", "only_own")
                      )

    _model = "right"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    write: Mapped[bool] = mapped_column(Boolean, default=False)
    read: Mapped[bool] = mapped_column(Boolean, default=False)
    only_own: Mapped[bool] = mapped_column(Boolean, default=True)

    model: Mapped[ModelName] = mapped_column(String(60), nullable=False)

    @property
    def dict(self):
        return {
            "id": self.id,
            "write": self.write,
            "read": self.read,
            "only_own": self.only_own,
            "model": self.model,
        }


class Role(Base):
    __tablename__ = "role"
    _model = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    rights: Mapped[list[Right]] = relationship(secondary=role_rights, lazy="joined")

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "rights": [right.id for right in self.rights]
        }


class User(Base):
    __tablename__ = 'user'
    _model = "user"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    tokens: Mapped[list["Token"]] = relationship("Token", back_populates='user', lazy="joined",
                                                 cascade="all, delete-orphan")
    advertisements: Mapped[list["Advertisement"]] = relationship("Advertisement", back_populates="user",
                                                                 lazy="joined", cascade="all, delete-orphan")
    roles: Mapped[list[Role]] = relationship(secondary=user_roles, lazy="joined")

    @property
    def dict(self):
        return {
            "user_id": self.user_id,
            "login": self.login,
        }


class Token(Base):
    __tablename__ = "token"
    _model = "token"
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(UUID, server_default=func.gen_random_uuid(), unique=True)
    creation_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), nullable=False)
    user: Mapped[User] = relationship("User", lazy="joined", back_populates="tokens")

    @property
    def dict(self):
        return {"token": self.token}


class Advertisement(Base):
    __tablename__ = 'advertisement'
    _model = 'advertisement'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    user: Mapped[User] = relationship("User", back_populates='advertisements', lazy="joined")

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "user": self.user.dict,
        }


MODEL = User | Advertisement | Token
MODEL_CLS = Type[User] | Type[Advertisement] | Type[Token]
