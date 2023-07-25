import time
from collections.abc import Callable
from enum import Enum
from typing import Annotated

from fastapi import Body, Cookie, FastAPI, Header, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr, HttpUrl

app = FastAPI()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Image(BaseModel):
    url: HttpUrl
    name: str


# class Item(BaseModel):
#     name: str = Field(examples=["Foo"])
#     description: str | None = Field(
#         default=None,
#         title="The description of the item",
#         min_length=10,
#         max_length=300,
#         examples=["A very nice item"],
#     )
#     price: float = Field(
#         gt=0, description="The price must be greater than zero", examples=[35.4]
#     )
#     tax: float | None = Field(default=None, examples=[2.02])
#     tags: list[str] = Field(examples=[["blues", "soul"]])
#     image: list[Image] | None = None

# model_config = {
#     "json_schema_extra": {
#         "examples": [
#             {
#                 "name": "Foo",
#                 "description": "A very nice Item",
#                 "price": 35.4,
#                 "tax": 3.2,
#                 "tags": ["rock", "soul"],
#                 "image": [
#                     {
#                         "url": "https://www.images.com/blah",
#                         "name": "Blah image",
#                     },
#                     {
#                         "url": "https://www.images.com/bingo",
#                         "name": "bingo image",
#                     },
#                 ],
#             }
#         ]
#     }
# }


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


class User(BaseModel):
    username: str
    full_name: str | None = None


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights


@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images


# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: str | None = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item


# @app.post("/items/")
# async def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict


# @app.get("/items/")
# async def read_items(
#     # q: Annotated[list | None, Query()] = ["xxx", "yyy"]
#     ads_id: Annotated[str | None, Cookie()] = None,
#     q: Annotated[
#         str | None,
#         Query(
#             title="Query string",
#             alias="item-query",
#             description="hello there",
#             min_length=3,
#             deprecated=True,
#         ),
#     ] = None,
#     hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None,
# ):
#     results: dict = {}
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if ads_id:
#         results.update({"ads_id": ads_id})
#     if q:
#         results.update({"q": q})
#     if hidden_query:
#         results.update({"hidden_query": hidden_query})
#     else:
#         results.update({"hidden_query": "Not found"})
#     return results


# @app.put("/items/{item_id}")
# async def read_items(
#     item_id: UUID,
#     start_datetime: Annotated[datetime | None, Body()] = None,
#     end_datetime: Annotated[datetime | None, Body()] = None,
#     repeat_at: Annotated[time | None, Body()] = None,
#     process_after: Annotated[timedelta | None, Body()] = None,
# ):
#     start_process = start_datetime + process_after
#     duration = end_datetime - start_process
#     return {
#         "item_id": item_id,
#         "start_datetime": start_datetime,
#         "end_datetime": end_datetime,
#         "repeat_at": repeat_at,
#         "process_after": process_after,
#         "start_process": start_process,
#         "duration": duration,
#     }


# @app.put("/items/{item_id}")
# async def create_item(
#     item_id: Annotated[
#         int,
#         Path(
#             title="The ID of the item to get",
#             description="hello item id",
#             gt=0,
#             le=5000,
#         ),
#     ],
#     item: Annotated[Item, Body(embed=True)],
#     user: User,
#     # importance: Annotated[int, Body(gt=0)],
#     q: str | None = None,
# ):
#     result = {
#         "item_id": item_id,
#         "item": item,
#         #   **item.model_dump(),
#         "user": user,
#     }
#     if q:
#         result.update({"q": q})

#     return result


# @app.get("/items/{item_id}")
# async def read_item(
#     item_id: str,
#     needy: str,
#     skip: int = 0,
#     limit: int | None = None
# ):
#     item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
#     return item


# @app.get("/items/")
# async def read_items() -> list[Item]:
#     return [
#         Item(name="Portal Gun", price=42.0, tags=[]),
#         Item(name="Plumbus", price=32.0, tags=[]),
#     ]


# @app.get("/items/", response_model=list[Item])
# async def read_items() -> Any:
#     return [
#         {"name": "Portal Gun", "price": 42.0, "tags": []},
#         {"name": "Plumbus", "price": 32.0, "tags": []},
#     ]


# @app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
# async def read_item(item_id: str):
#     return items[item_id]


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]


# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]


# @app.get("/items/header/")
# async def read_items_header(
#     strange_header: Annotated[str | None, Header(convert_underscores=False)] = None
# ):
#     return {"strange_header": strange_header}


@app.get("/items/headers/")
async def read_items_headers(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}


@app.get("/items/cookie/")
async def read_items_cookie(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


@app.get("/portal", response_model=None)
async def get_portal(*, teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}


# @app.get("/portal")
# async def get_portal(teleport: bool = False) -> Response | dict:
#     if teleport:
#         return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
#     return JSONResponse(content={"message": "Here's your interdimensional portal."})


@app.get("/teleport")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")


@app.put("/items/update/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Bar",
                    "description": "A very nice updated Item",
                    "price": 33.333,
                    "tax": 3.1415,
                    "tags": ["jazz", "trance"],
                    "image": [
                        {"url": "https://example.com/bizzaro", "name": "bizzaro"}
                    ],
                },
                {
                    "name": "Bar",
                    "description": "Item with no images and 20% vat",
                    "price": 120.00,
                    "tax": 20.0,
                    "tags": ["chamber"],
                    "image": [],
                },
            ],
        ),
    ],
):
    return {"item_id": item_id, "item": item}


# @app.post("/user/", response_model=UserOut)
# async def create_user(user: UserIn) -> Any:
#     return user


@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, *, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
