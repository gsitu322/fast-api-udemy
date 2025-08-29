from fastapi import FastAPI

app = FastAPI()

books = {
    "title": "Title one", "author": "Author one",
}

@app.get("/books")
async def first_api():
    return {"message": "Hello World"}