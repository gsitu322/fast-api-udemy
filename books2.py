from fastapi import FastAPI

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