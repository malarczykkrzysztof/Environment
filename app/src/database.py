from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError
from fastapi import HTTPException
from typing import List, Dict
from app.models.user import User 
from app.models.user import UserSafe

class Database():
    def __init__(self) -> None: 
        client = MongoClient("mongodb://mongoadmin:LikeAndSubscribe@mongo:27017/")
        try:
            client.server_info()
        except ServerSelectionTimeoutError as e:
            raise HTTPException(status_code=503, detail="Problem with connecting to database")
        self.users_collection = client["data"]["users"]
        
    def get_all_users(self) -> List[UserSafe]:
        """Method for fetching data from mongoDB about all users

        Returns:
            List[UserSafe]: Returns list of users in UserSafe model format
        """  
        results = self.users_collection.find({})
        return list(results)
    
    def get_one_user(self, user_email: str)-> UserSafe:
        """Method for fetching data about user based on e-mail from mongoDB

        Returns:
            UserSafe: Returns user in UserSafe model format
        """  
        
        user_data = self.users_collection.find_one({"email": user_email})
        if user_data is None: 
            raise HTTPException(status_code=404, detail=f"User with {user_email} not found in database")
        return user_data
        
    def user_update(self, user: User) -> Dict[str, str]:
        """Method for updating user data based on e-mail from mongoDB

        Returns:
            Dict[str, str]
        """  
        results= self.users_collection.replace_one({"email": user.email}, user.model_dump())
        if not results.modified_count:
            raise HTTPException(status_code=404, detail=f"User with {user.email} not found in database")
        return {"Info ": f"User with email {user.email}modified in db"}
    
    def add_user(self, user: User) -> Dict[str, str]:
        """Method for adding user data based to mongoDB

        Returns:
            Dict[str, str]
        """      
        try:
            self.users_collection.insert_one(user.model_dump())
        except DuplicateKeyError:
            raise HTTPException(status_code=409, detail=f"User with email {user.email} not created: duplicated")
        return {"Info ": f"User with email {user.email} added in db"}
    
    def delete_user(self, user_email: str)-> Dict[str, str]:
        """Method for clear data user based on e-mail from our mongoDB

        Returns:
            Dict[str, str]
        """ 
        user_data = self.users_collection.delete_one({"email": user_email})
        if not user_data.deleted_count:
            raise HTTPException(status_code=404, detail=f"User with {user_email} not found in database")    
        return {"Info: " f"User with email {user_email} removed in db"}
    
    def delete_users(self) -> Dict[str, str]:
        """Method for clear our mongoDB

        Returns:
            Dict[str, str]
        """ 
        result = self.users_collection.delete_many({})
        return {"Info ": f"Deleted {result.deleted_count} users from DB"}
    
    
    def add_users(self) -> List[UserSafe]:
        """Method for add predefined users to mongoDB

        Returns:
            >List[UserSafe]
        """ 
        
        def create_one(firs_name: str, last_name: str, email: str, password: str):
            test_dict = {
                "first_name": firs_name,
                "last_name": last_name,
                "email": email,
                "password": password
            }
            self.users_collection.insert_one(test_dict)
            
        create_one("Jan", "Kowalski", "Jan.Kowalski@email.com", "SomePass")
        create_one("Krzysztof", "AAA", "Krzysztof.AAA@email.com", "SomePass")
        create_one("Piotr", "BBB", "Piotr.BBB@email.com", "SomePass")
        create_one("Pawel", "CCC", "Pawel.CCC@email.com", "SomePass")
        results = self.users_collection.find({})
        return list(results)
