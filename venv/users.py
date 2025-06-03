from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import List, Optional
class USER(BaseModel):
    name: str
    age: int
    sexe: str
    password: str
    
    
app=FastAPI()
user_db: List[USER] = []

@app.get("/")
def read_root():
    return {"Hello":"USER"}

@app.get("/users")
async def read_all_users():
    all_users = [user for user in user_db]
    return all_users

    

@app.get("/users/all_users")
async def read_all_users():
    return {'user_name': 'user'}

@app.get("/users/{dynamic_param}")
async def read_all_users(dynamic_param):
    return {'dynamic_param': dynamic_param}

@app.post("/users/create_user")
async def create_book(new_book: Book):
    new_book.id = len(books_db) +1
    books_db.append(new_book)
    return {"message": "Book created successfully", "book": new_book}

@app.put("/books/update_book/{book_id}")
async def update_book(book_id: int, updated_book: Book):
    for i , book in enumerate(books_db):
        if book.id == book_id:
            updated_book.id = book_id
            books_db[i] = updated_book
            return {"message": f"BOOK with id {book_id} has been updated", "book": updated_book}
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

@app.delete("/books/delete_book/{book_id}")
async def delete_book(book_id: int):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            del books_db[i]
            return {"message": f"BOOK with id {book_id} has been deleted"}
    raise HTTPException(status_code=404, detail=("BOOK with id {book_id} not found"))

@app.patch("/books/patch/{book_id}")
async def patch_book(book_id: int, patch_data: Book):
    stored_book_data = None
    for book in books_db:
        if book.id == book_id:
            stored_book_data == book
            update_data = patch_data.dict(exclude_unset= True)
            updated_book = stored_book_data.copy(update=update_data)
            books_db[books_db.index(book)] = update_book
            return {"message":f"BOOK with id {book_id} has been patched", "book": updated_book}
    if stored_book_data is None:
        raise  HTTPException(status_code=404, detail=("BOOK with id {book_id} not found"))