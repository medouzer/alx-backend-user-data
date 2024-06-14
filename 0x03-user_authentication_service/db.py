#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError, SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

import logging

from user import Base, User
logging.disable(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """create user"""
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        try:
            session.add(new_user)
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """find user"""
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()

    def update_user(self, user_id: int, **kwargs) -> None:
        """update the user"""
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError("User with id {} not found".format(user_id))
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError("User has no attribute {}".format(key))
            setattr(user, key, value)
        try:
            self._session.commit()
        except InvalidRequestError:
            raise ValueError("Invalid request")
