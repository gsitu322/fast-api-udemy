from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not required on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Gordon",
                "description": "A description of a book",
                "rating": 5
            }
        }
    }


books = [
    Book(1, "Computer Science Pro", "Gordon", "Some Description", 5),
    Book(2, "My Story", "Max", "His story", 3),
    Book(3, "Be Fast with FastAPI", "Roby", "FastAPI", 4),
    Book(4, "Be Slow with FastAPI", "Roby", "Slow FastAPI", 1),
    Book(5, "Python's Best Seller", "Python", "List of python best sellers", 4),
    Book(6, "Harry Potter 1", "JK Rowling", "Harry Potter", 5),
]

@app.get("/books")
async def read_all_books():
    return books

@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in books:
        if (book.id == book_id):
            return book

@app.get("/books/")
async def read_book_by_rating(book_rating: int):
    books_to_return = []
    for book in books:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return

@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    books.append(find_book_id(new_book))

@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(books)):
        if books[i].id == book.id:
            books[i] = book

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(books)):
        if books[i].id == book_id:
            books.pop(i)
            break

def find_book_id(book: Book):
    book.id = 1 if len(books) == 0 else books[-1].id + 1
    return book