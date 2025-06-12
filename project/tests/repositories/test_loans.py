import pytest
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.models.loans import Loan
from src.models.books import Book
from src.models.users import User
from src.repositories.loans import LoanRepository
from src.repositories.books import BookRepository
from src.repositories.users import UserRepository


def create_user_and_book(db_session):
    user_repo = UserRepository(User, db_session)
    book_repo = BookRepository(Book, db_session)

    user = user_repo.create({"email": "testuser@example.com", "hashed_password": "hashed", "is_active": True})
    book = book_repo.create({
        "title": "Test Book",
        "author": "Author",
        "isbn": "0000000000000",
        "publication_year": 2023,
        "quantity": 1
    })

    return user, book


def test_create_loan(db_session: Session):
    """
    Teste la création d'un emprunt.
    """
    loan_repo = LoanRepository(Loan, db_session)
    user, book = create_user_and_book(db_session)

    loan_data = {
        "user_id": user.id,
        "book_id": book.id,
        "loan_date": datetime.utcnow(),
        "due_date": datetime.utcnow() + timedelta(days=7)
    }

    loan = loan_repo.create(obj_in=loan_data)

    assert loan.id is not None
    assert loan.user_id == user.id
    assert loan.book_id == book.id


def test_get_active_loans(db_session: Session):
    """
    Teste la récupération des emprunts actifs.
    """
    repo = LoanRepository(Loan, db_session)
    user, book = create_user_and_book(db_session)

    repo.create({
        "user_id": user.id,
        "book_id": book.id,
        "loan_date": datetime.utcnow(),
        "due_date": datetime.utcnow() + timedelta(days=7),
        "return_date": None
    })

    active_loans = repo.get_active_loans()
    assert len(active_loans) >= 1
    assert all(loan.return_date is None for loan in active_loans)


def test_get_overdue_loans(db_session: Session):
    """
    Teste la récupération des emprunts en retard.
    """
    repo = LoanRepository(Loan, db_session)
    user, book = create_user_and_book(db_session)

    overdue_loan = repo.create({
        "user_id": user.id,
        "book_id": book.id,
        "loan_date": datetime.utcnow() - timedelta(days=10),
        "due_date": datetime.utcnow() - timedelta(days=5),
        "return_date": None
    })

    overdue_loans = repo.get_overdue_loans()
    assert any(loan.id == overdue_loan.id for loan in overdue_loans)


def test_get_loans_by_user_and_book(db_session: Session):
    """
    Teste la récupération des emprunts par utilisateur et par livre.
    """
    repo = LoanRepository(Loan, db_session)
    user, book = create_user_and_book(db_session)

    repo.create({
        "user_id": user.id,
        "book_id": book.id,
        "loan_date": datetime.utcnow(),
        "due_date": datetime.utcnow() + timedelta(days=7)
    })

    loans_by_user = repo.get_loans_by_user(user_id=user.id)
    loans_by_book = repo.get_loans_by_book(book_id=book.id)

    assert loans_by_user
    assert loans_by_book
    assert loans_by_user[0].user_id == user.id
    assert loans_by_book[0].book_id == book.id


def test_get_with_details(db_session: Session):
    """
    Teste la récupération d’un emprunt avec les détails utilisateur et livre.
    """
    repo = LoanRepository(Loan, db_session)
    user, book = create_user_and_book(db_session)

    loan = repo.create({
        "user_id": user.id,
        "book_id": book.id,
        "loan_date": datetime.utcnow(),
        "due_date": datetime.utcnow() + timedelta(days=7)
    })

    detailed = repo.get_with_details(id=loan.id)

    assert detailed is not None
    assert detailed.user.email == user.email
    assert detailed.book.title == book.title


def test_get_loans_stats(db_session: Session):
    """
    Teste la récupération des statistiques d'emprunts.
    """
    repo = LoanRepository(Loan, db_session)
    user, book = create_user_and_book(db_session)

    repo.create({
        "user_id": user.id,
        "book_id": book.id,
        "loan_date": datetime.utcnow() - timedelta(days=10),
        "due_date": datetime.utcnow() - timedelta(days=2),
        "return_date": None
    })

    stats = repo.get_loans_stats()

    assert "total_loans" in stats
    assert "active_loans" in stats
    assert "overdue_loans" in stats
    assert "loans_by_month" in stats
    assert isinstance(stats["loans_by_month"], dict)
