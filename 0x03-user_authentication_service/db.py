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
        """Search and return user by a given field.

        Args:
            **kwargs: Arbitrary keyword arguments representing user attributes.

        Raises:
            InvalidRequestError: If no keyword arguments are provided or if
             any provided key is not a valid user attribute.
            NoResultFound: If no user is found with the given attributes.

        Returns:
            User: The user object that matches the given attributes.
        """
        if not kwargs:
            raise InvalidRequestError("No search parameters provided.")

        if not self._valid_attributes(**kwargs):
            raise InvalidRequestError("Invalid search parameters provided.")

        db_user = self._session.query(User).filter_by(**kwargs).first()
        if not db_user:
            raise NoResultFound("No user found with the given parameters.")

        return db_user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update an instance of a user.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing user attributes
             to update.

        Raises:
            ValueError: If any provided key is not a valid user attribute.
        """
        if not self._valid_attributes(**kwargs):
            raise ValueError("Unrecognized arguments for User.")

        db_user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            setattr(db_user, key, value)

        self._session.add(db_user)
        self._session.commit()

    def delete_user_by_id(self, user_id: int) -> None:
        """Delete a user from the database by user ID

        Args:
            user_id (int): The user ID.
        """
        user = self.find_user_by(id=user_id)
        self._session.delete(user)
        self._session.commit()
