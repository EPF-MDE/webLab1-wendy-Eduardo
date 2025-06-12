import pytest
from sqlalchemy.orm import Session

from src.models.users import User
from src.repositories.users import UserRepository


def test_create_user(db_session: Session):
    """
    Teste la création d'un utilisateur.
    """
    repo = UserRepository(User, db_session)

    user_data = {
        "email": "user@example.com",
        "hashed_password": "hashed_pwd",
        "is_active": True
    }

    user = repo.create(obj_in=user_data)

    assert user.id is not None
    assert user.email == "user@example.com"
    assert user.hashed_password == "hashed_pwd"
    assert user.is_active is True


def test_get_by_email(db_session: Session):
    """
    Teste la récupération d’un utilisateur par email.
    """
    repo = UserRepository(User, db_session)

    email = "lookup@example.com"
    user_data = {
        "email": email,
        "hashed_password": "lookup_pwd",
        "is_active": True
    }

    repo.create(obj_in=user_data)

    user = repo.get_by_email(email=email)

    assert user is not None
    assert user.email == email
    assert user.hashed_password == "lookup_pwd"
