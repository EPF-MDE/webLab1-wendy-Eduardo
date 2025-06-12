import pytest
from sqlalchemy.orm import Session

from src.models.categories import Category
from src.repositories.categories import CategoryRepository


def test_create_category(db_session: Session):
    """
    Teste la création d'une catégorie.
    """
    repo = CategoryRepository(Category, db_session)

    category_data = {"name": "TestCategory", "description": "Test description"}
    category = repo.create(obj_in=category_data)

    assert category.id is not None
    assert category.name == "TestCategory"
    assert category.description == "Test description"


def test_get_by_name_existing(db_session: Session):
    """
    Teste la récupération d'une catégorie existante par nom.
    """
    repo = CategoryRepository(Category, db_session)

    # Créer une catégorie
    category_data = {"name": "ExistingCategory", "description": "Existing"}
    created = repo.create(obj_in=category_data)

    # Rechercher
    category = repo.get_by_name(name="ExistingCategory")

    assert category is not None
    assert category.id == created.id
    assert category.name == "ExistingCategory"


def test_get_by_name_nonexistent(db_session: Session):
    """
    Teste la récupération d'une catégorie inexistante.
    """
    repo = CategoryRepository(Category, db_session)

    category = repo.get_by_name(name="NonexistentCategory")
    assert category is None


def test_get_or_create_existing(db_session: Session):
    """
    Teste get_or_create quand la catégorie existe déjà.
    """
    repo = CategoryRepository(Category, db_session)

    existing = repo.create(obj_in={"name": "Reusable", "description": "Reuse test"})

    result = repo.get_or_create(name="Reusable")

    assert result.id == existing.id
    assert result.name == "Reusable"


def test_get_or_create_new(db_session: Session):
    """
    Teste get_or_create quand la catégorie n'existe pas.
    """
    repo = CategoryRepository(Category, db_session)

    result = repo.get_or_create(name="NewCategory", description="Newly created")

    assert result is not None
    assert result.id is not None
    assert result.name == "NewCategory"
    assert result.description == "Newly created"
