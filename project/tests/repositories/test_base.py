import pytest
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.models.base import Base
from src.repositories.base import BaseRepository

# Modèle SQLAlchemy fictif pour test
class Dummy(Base):
    __tablename__ = "dummy"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Schéma Pydantic pour création/mise à jour
class DummyCreate(BaseModel):
    name: str

class DummyUpdate(BaseModel):
    name: str

@pytest.fixture
def dummy_repo(db_session: Session):
    return BaseRepository[Dummy, DummyCreate, DummyUpdate](Dummy, db_session)

def test_create(dummy_repo: BaseRepository, db_session: Session):
    obj_in = DummyCreate(name="test")
    obj = dummy_repo.create(obj_in=obj_in)
    assert obj.id is not None
    assert obj.name == "test"

def test_get(dummy_repo: BaseRepository, db_session: Session):
    obj_in = DummyCreate(name="test_get")
    obj = dummy_repo.create(obj_in=obj_in)
    fetched = dummy_repo.get(id=obj.id)
    assert fetched is not None
    assert fetched.name == "test_get"

def test_get_multi(dummy_repo: BaseRepository, db_session: Session):
    for i in range(5):
        dummy_repo.create(obj_in=DummyCreate(name=f"name{i}"))
    objs = dummy_repo.get_multi(skip=0, limit=10)
    assert len(objs) >= 5

def test_update(dummy_repo: BaseRepository, db_session: Session):
    obj_in = DummyCreate(name="old_name")
    obj = dummy_repo.create(obj_in=obj_in)
    update_in = DummyUpdate(name="new_name")
    updated = dummy_repo.update(db_obj=obj, obj_in=update_in)
    assert updated.name == "new_name"

def test_remove(dummy_repo: BaseRepository, db_session: Session):
    obj_in = DummyCreate(name="to_delete")
    obj = dummy_repo.create(obj_in=obj_in)
    removed = dummy_repo.remove(id=obj.id)
    assert removed.id == obj.id
    assert dummy_repo.get(id=obj.id) is None
