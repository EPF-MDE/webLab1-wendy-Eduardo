from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...models.categories import Category as CategoryModel
from ..schemas.books import Category  # reutiliza el esquema si ya está hecho
from ...repositories.categories import CategoryRepository
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Category])
def read_categories(db: Session = Depends(get_db)):
    repo = CategoryRepository(CategoryModel, db)
    return repo.get_multi()