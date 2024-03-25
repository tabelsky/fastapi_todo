from fastapi import FastAPI
from schema import TodoItem

app = FastAPI(title='Todo API', version='1.0', description='A simple TODO API')





@app.get("/todo/{item_id}", tags=["todo item"])
def get_todo(item_id: int) -> TodoItem:
    return TodoItem(title="Foo", description="The Foo Wrestlers")


@app.get("/todo/", tags=["todo items"])
def search_todo(title: str = None, description = None) -> TodoItem:

    return TodoItem(title=title or '1', description=description or '2')


@app.post("/todo/", tags=["todo item"])
def create_todo(item: TodoItem) -> TodoItem:

    ...
    return item