from fastapi import FastAPI, HTTPException
from my_models import User, UserIn_Pydantic, User_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from passlib.hash import bcrypt
import uvicorn


app = FastAPI()
@app.get('/')
async def read_root():
    return {"Hello": "World"}

@app.get("/allusers")
async def get_allusers():
    return await User_Pydantic.from_queryset(User.all())

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))

@app.post("/createuser",response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = await User.create(**user.dict(exclude_unset=True))
    # user_obj.password_hash = bcrypt.hash(user.password_hash)
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

@app.put('/updateuser/{user_id}', response_model=User_Pydantic)
async def update_user(user_id: int, user: UserIn_Pydantic):
    # user.password_hash = bcrypt.hash(user.password_hash)
    # await User.get(id=user_id).update(**user.dict(exclude_unset=True))
    await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))

@app.delete('/deleteuser/{user_id}')
async def delete_user(user_id: int):
    await User.filter(id=user_id).delete()
    return {"msg": "Deleted Sucessfully "}

register_tortoise(
    app,
    db_url="sqlite://usersdatabase.db",
    modules={'models':['my_models']},
    generate_schemas = True,
    add_exception_handlers = True,
)

if __name__ == '__main__':
    uvicorn.run(app,port=8000 , host="0.0.0.0")