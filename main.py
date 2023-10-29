from enum import Enum
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
import uvicorn

from time import time

app = FastAPI()


class DogType(str, Enum):
    terrier = 'terrier'
    bulldog = 'bulldog'
    dalmatian = 'dalmatian'


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind='bulldog'),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]

valid_dog_types = [item.value for item in list(DogType)]


@app.get('/')
def root():
    return {'message': 'Привет, это микросервис для хранения и обновления информации для собак!'}


@app.post("/post")
def get_post():
    time_stamp = Timestamp(id=len(post_db) + 1, timestamp=int(time()))
    post_db.append(time_stamp)
    return time_stamp


@app.get("/dog")
def get_dogs(kind: DogType):
    return {k: v for (k, v) in dogs_db.items() if v.kind == kind}


@app.post("/dog")
def create_dog(dog: Dog):
    if dog.pk in dogs_db.keys():
        raise HTTPException(status_code=422, detail='Pk already exist')
    else:
        dogs_db[dog.pk] = dog
        post_db.append(Timestamp(id=len(post_db) + 1, timestamp=int(time())))
        return dog


@app.get("/dog/{pk}")
def get_dog_by_pk(pk: int):
    if pk not in dogs_db.keys():
        raise HTTPException(status_code=422, detail='Pk not found')
    else:
        return dogs_db[pk]


@app.patch("/dog/{pk}")
def update_dog(pk: int, dog: Dog):
    if pk not in dogs_db.keys():
        raise HTTPException(status_code=422, detail='Pk not found')
    else:
        dogs_db[pk] = dog
        post_db.append(Timestamp(id=len(post_db) + 1, timestamp=int(time())))
        return dog


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
