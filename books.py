from fastapi import FastAPI, Body

app = FastAPI()

books = [
    {"title": "Title one", "author": "Author one", "category": "science"},
    {"title": "Title two", "author": "Author two", "category": "science"},
    {"title": "Title three", "author": "Author three", "category": "history"},
    {"title": "Title four", "author": "Author four", "category": "math"},
    {"title": "Title five", "author": "Author five", "category": "math"},
    {"title": "Title six", "author": "Author two", "category": "math"}
]

@app.get("/books")
async def read_all_books():
    return books

@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in books:
        if book.get("title").casefold() == book_title.casefold():
            return book

    return None

@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []

    for book in books:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return

@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author:str, category: str):
    books_to_return = []

    for book in books:
        if book.get("author").casefold() == book_author.casefold() and book.get("category").casefold() == category.casefold() :
            books_to_return.append(book)

    return books_to_return

@app.post("/books/create_book")
async def create_book(new_book = Body(...)):
    books.append(new_book)
