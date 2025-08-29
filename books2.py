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
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)


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


@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    books.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(books) == 0 else books[-1].id + 1
    return book