from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    publish_date: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int, publish_date: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not required on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    publish_date: int = Field(gt=1999, lt=2030)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Gordon",
                "description": "A description of a book",
                "rating": 5,
                "publish_date": 2025
            }
        }
    }


books = [
    Book(1, "Computer Science Pro", "Gordon", "Some Description", 5, 2021),
    Book(2, "My Story", "Max", "His story", 3, 2022),
    Book(3, "Be Fast with FastAPI", "Roby", "FastAPI", 4, 2015),
    Book(4, "Be Slow with FastAPI", "Roby", "Slow FastAPI", 1, 2015),
    Book(5, "Python's Best Seller", "Python", "List of python best sellers", 4, 2007),
    Book(6, "Harry Potter 1", "JK Rowling", "Harry Potter", 5, 2004),
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return books

@app.get("/books/bypublushDate/", status_code=status.HTTP_200_OK)
async def read_book_by_publish_date(publish_date: int = Query(gt=1999, lt=2030)):
    books_to_return = []

    for book in books:
        if book.publish_date == publish_date:
            books_to_return.append(book)

    return books_to_return

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in books:
        if (book.id == book_id):
            return book

    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in books:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return

@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    books.append(find_book_id(new_book))

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False

    for i in range(len(books)):
        if books[i].id == book.id:
            books[i] = book
            book_changed = True

    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False

    for i in range(len(books)):
        if books[i].id == book_id:
            books.pop(i)
            book_deleted = True
            break

    if not book_deleted:
        raise HTTPException(status_code=404, detail="Book not found")

def find_book_id(book: Book):
    book.id = 1 if len(books) == 0 else books[-1].id + 1
    return book