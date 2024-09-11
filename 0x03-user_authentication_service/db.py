#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy.orm.exc import NoResultFound, InvalidRequestError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


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
        """Add a new user to the database

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The User object that was added to the database.
        """
        # Create a new User object with the provided email and hashed_password
        new_user = User(email=email, hashed_passowrd=hashed_password)

        #add user to session
        self._session.add(new_user)

        # Commit the session to save the user in the database
        self._session.commit()

        return new_user
    
    def find_user_by(self, **kwargs) -> User:
        """Find a user by a specific attribute

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            User: The first row that matches the query.
        """
        try:
            # Query the database for a user that matches the kwargs
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            # If no user is found, return None
            raise NoResultFound

        except InvalidRequestError: # If the query is not valid
            raise InvalidRequestError
        
    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user in the database

        Args:
            user_id (int): The user ID.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)
        self._session.commit()

    def delete_user_by_id(self, user_id: int) -> None:
        """Delete a user from the database by user ID

        Args:
            user_id (int): The user ID.
        """
        user = self.find_user_by(id=user_id)
        self._session.delete(user)
        self._session.commit()
