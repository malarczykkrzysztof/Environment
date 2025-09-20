from fastapi import FastAPI, status
from typing import List
from pymongo import MongoClient
from app.models.message import Message
from app.models.user import User 
from app.models.user import UserSafe
from app.src.database import Database

app = FastAPI()

@app.get("/user",response_model=List[UserSafe],tags=["users"])
def users_all():
    """Get all users from database"""   
    return Database().get_all_users()

@app.get("/users/{user_email}",response_model= UserSafe, tags=["users"])
def users_one(user_email: str):
    """Get user from database by e-mail"""    
    return Database().get_one_user(user_email)  

@app.put("/users", tags=["users"])
def user_update(user: User):
    """Update user to database """ 
    return Database().user_update(user)
    
@app.post("/users",status_code = status.HTTP_201_CREATED, tags= ["users"], responses= {409: {"model": Message}})
def add_user(user: User):  
    """Add new user to database"""
    return Database().add_user(user)
    
@app.delete("/users/{user_email}", tags=['users'])
def delete_user_by_email(user_email: str):
    """Delete user from database by e-mail"""
    return Database().delete_user(user_email)

@app.delete("/users/", tags=['users'])
def delete_all():
    """Delete all users from database """
    return Database().delete_users()

@app.post("/users/",status_code = status.HTTP_201_CREATED, tags= ["users"])
def add_users()-> List[UserSafe]:  
    """Add user from list to database"""
    return Database().add_users()
    
# def create_index():
#     client = MongoClient("mongodb://mongoadmin:LikeAndSubscribe@mongo:27017/")
#     test_collection = client["data"]["users"]
#     test_collection.create_index("email",unique = True)  
    
# def list_indexes():
#     client = MongoClient("mongodb://mongoadmin:LikeAndSubscribe@mongo:27017/") 
#     test_collection = client["data"]["users"]
#     result = test_collection.list_indexes()
#     for index in result:
#         print (index)

# create_index()
# list_indexes()