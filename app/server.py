from fastapi import FastAPI, Request, Depends, Header
import datetime
from uuid import UUID
import bcrypt
import schema
from typing import Annotated
from contextlib import asynccontextmanager
from models import init_db, User, Token, Role, Right, Todo
from models import Session
from sqlalchemy import select
from fastapi.exceptions import HTTPException
from sqlalchemy import func
TOKEN_TTL = 60
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup")
    await init_db()
    async with Session() as session:
        hashed_password = bcrypt.hashpw('admin'.encode(), bcrypt.gensalt())
        user = User(name="admin", password=hashed_password.decode())
        session.add(user)
        await session.commit()
        role = Role(name="admin")
        session.add(role)
        await session.commit()

        for model in [User, Token, Todo, Role, Right]:
            right = Right(model=model.__name__, read=True, write=True, only_own=False)
            session.add(right)
            await session.commit()
        todo = Todo(name="test", user=user)
        session.add(todo)
        right = await check_objetct_right(user, todo, write=True, db_session=session)
        await session.commit()
    yield
    print("Shutdown")

app = FastAPI(title='Todo API', version='1.0', description='A simple TODO API', lifespan=lifespan)

async def get_db_session():
    async with Session() as session:
        yield session

async def check_token(token: Annotated[UUID, Header()], db_session = Depends(get_db_session)):
    token = await db_session.scalar(select(Token).where(
        Token.token == token,
        Token.creation_time >= (func.now() - datetime.timedelta(seconds=TOKEN_TTL))
    ))
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

ORM_OBJECTS = [User, Token, Todo, Role, Right]
async def check_objetct_right(
        user: User,
        orm_object: ORM_OBJECTS,
        write: bool = False,
        read: bool = False,
        db_session = Session
):
    where_args = [Right.model == orm_object.__class__.__name__]

    is_owner = hasattr(orm_object, 'user_id') and orm_object.user_id == user.id
    if not is_owner:
        where_args.append(Right.only_own == False)
    if read:
        where_args.append(Right.read == True)
    if write:
        where_args.append(Right.write == True)

    right = await db_session.scalar(
        select(Right).where(
            *where_args
        ).limit(1),
    )
    if right is None:
        raise HTTPException(status_code=403, detail="No rights")
    return right

def get_current_user(token=Depends(check_token)):
    return token.user

@app.post('/user')
async def create_user(user: schema.CreateUser, db_session = Depends(get_db_session)) -> schema.UserResponse:
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    user = User(name=user.username, password=hashed_password.decode())
    db_session.add(user)
    await db_session.commit()
    return schema.UserResponse(id=user.id, username=user.name, registration_time=user.registration_time)


@app.post('/login')
async def login(login_data: schema.Login, db_session = Depends(get_db_session)) -> schema.Token:
    user = await db_session.scalar(select(User).where(User.name == login_data.username))
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not bcrypt.checkpw(login_data.password.encode(), user.password.encode()):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = Token(user=user)
    db_session.add(token)
    await db_session.commit()
    return token


@app.get("/todo/{item_id}", tags=["todo item"])
def get_todo(item_id: int) -> schema.CreateTodoItem:
    return schema.CreateTodoItem(title="Foo", description="The Foo Wrestlers")


@app.get("/todo/", tags=["todo items"])
def search_todo(title: str = None, description = None) -> schema.CreateTodoItem:

    return schema.CreateTodoItem(title=title or '1', description=description or '2')


@app.post("/todo/", tags=["todo item"])
def create_todo(
        item: schema.CreateTodoItem,
        db_session=Depends(get_db_session),
        user=Depends(get_current_user)) -> schema.CreateTodoItem:
    ...
    return item
