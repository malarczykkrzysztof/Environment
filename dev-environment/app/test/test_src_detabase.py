from src.database import Database
from unittest.mock import patch, Mock, MagicMock
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError
from fastapi import HTTPException
import pytest

from app.models.user import User 
from app.models.user import UserSafe


test_user1 = User( first_name= "Jan", last_name= "Kowalski", email= "Kowalski@Email.com", password= "mypassword")
test_user2 = User( first_name= "Piotr", last_name= "Malik", email= "Malik@Email.com", password= "malik")


mocked_db_data = [
    {
        "id": 1,
        "name": "SomeUser"
    },
    {
        "id": 2,
        "name": "SomeUser2"
    },
    {
        "id": 3,
        "name": "SomeUser3"
    }
]

mocked_db_data2 =[test_user1,test_user2]
        

@patch("src.database.MongoClient")
def test_Database_init(mocked_database):
    database_instance = MagicMock()
    database_instance.server_info.return_value = "Some server info"
    database_instance.__getitem__.return_value.__getitem__.return_value = mocked_db_data
    mocked_database.return_value = database_instance
    database_object = Database()
    assert database_object.users_collection == mocked_db_data
    
@patch("src.database.MongoClient")
def test_Database_init_error(mocked_database): 
    database_instance = Mock()
    database_instance.server_info.side_effect = ServerSelectionTimeoutError(message="Mocked Error")
    mocked_database.return_value = database_instance
    with pytest.raises(HTTPException) as e_info:
        Database()
    assert "status_code=503, detail='Problem with connecting to database" in str(e_info) 
    
    
@patch("src.database.MongoClient")
def test_Database_init_error2(mocked_database): 
    database_instance = Mock()
    database_instance.server_info.side_effect = TypeError()
    mocked_database.return_value = database_instance
    with pytest.raises(TypeError) as e_info:
        Database()
        

@pytest.fixture
def mocked_database_fix():
    with patch("src.database.MongoClient") as mocked_database:
        database_instance = MagicMock()
        database_instance.server_info.return_value = "Some server info"
        database_instance.__getitem__.return_value.__getitem__.return_value = mocked_db_data2
        mocked_database.return_value =  database_instance
        yield mocked_database
        
         
def test_database_init2(mocked_database_fix): 
    database_object = Database()
    assert database_object.users_collection == mocked_db_data2   

def test_database_get_all_users (mocked_database_fix):
    database_object = Database()
    mocked_collection = Mock()
    mocked_collection.find.return_value = test_user1
    database_object.users_collection = mocked_collection
    result = database_object.get_all_users()
    assert result == [('first_name', 'Jan'), ('last_name', 'Kowalski'), ('email', 'Kowalski@Email.com'), ('password', 'mypassword')]
    
def test_database_get_one_user (mocked_database_fix):
    database_object = Database()
    mocked_collection = Mock()
    mocked_collection.find_one.return_value = test_user1 
    database_object.users_collection = mocked_collection
    result = database_object.get_one_user(user_email = "MockedEmail")
    assert result == test_user1
    
def test_database_get_one_user_error (mocked_database_fix):
    database_object = Database()
    mocked_collection = Mock()
    mocked_collection.find_one.return_value = None
    database_object.users_collection = mocked_collection
    with pytest.raises(HTTPException) as e_info:
        database_object.get_one_user(user_email = 'MockedEmail')
    assert "status_code=404, detail='User with MockedEmail not found in database" in str(e_info) 
    
def test_database_user_update (mocked_database_fix):
    database_object = Database()
    mocked_user_data = Mock()
    mocked_user_data.modified_count = 1
    mocked_collection = Mock()
    mocked_collection.replace_one.return_value = mocked_user_data  
    database_object.users_collection = mocked_collection
   
    result = database_object.user_update(user = test_user1)
    
    assert result == {"Info ": f"User with email {test_user1.email}modified in db"}
      
def test_database_user_update_error (mocked_database_fix):
    database_object = Database()
    mocked_user_data = Mock()
    mocked_user_data.modified_count = 0
    mocked_collection = Mock() 
    mocked_collection.replace_one.return_value = mocked_user_data  
    database_object.users_collection = mocked_collection
   
    with pytest.raises(HTTPException) as e_info:
        database_object.user_update(user = test_user1)
    assert f"status_code=404, detail='User with {test_user1.email} not found in database" in str(e_info) 
    
    
    
    
def test_database_delete_user(mocked_database_fix):
    database_object = Database()
    mocked_user_data = Mock()
    mocked_user_data.deleted_count = 1
    mocked_collection = Mock()
    mocked_collection.delete_one.return_value = mocked_user_data  
    database_object.users_collection = mocked_collection
   
    result = database_object.delete_user(user_email = "MockedEmail")
    
    assert result == {"Info: " f"User with email MockedEmail removed in db"}
      
def test_database_delete_user_error (mocked_database_fix):
    database_object = Database()
    mocked_user_data = Mock() 
    mocked_user_data.deleted_count = 0
    mocked_collection = Mock() 
    mocked_collection.delete_one.return_value = mocked_user_data  
    database_object.users_collection = mocked_collection
   
    with pytest.raises(HTTPException) as e_info:
        database_object.delete_user(user_email = test_user1.email)
    assert f"status_code=404, detail='User with {test_user1.email} not found in database" in str(e_info)   
    
    
@pytest.fixture()
def mocked_collection_fix():
    mocked_user_data = Mock()
    mocked_user_data.deleted_count = 1
    mocked_user_data.modified_count = 1
    mocked_collection = Mock() 
    mocked_collection.delete_one.return_value = mocked_user_data
    mocked_collection.replace_one.return_value = mocked_user_data  
    return mocked_collection

@pytest.fixture()
def mocked_collection_fix_error():
    mocked_user_data = Mock()
    mocked_user_data.deleted_count = 1
    mocked_user_data.modified_count = 1
    mocked_collection = Mock() 
    mocked_collection.insert_one.side_effect = DuplicateKeyError(error ="MockedError")
    # mocked_collection.delete_one.return_value = mocked_user_data
    # mocked_collection.replace_one.return_value = mocked_user_data  
    return mocked_collection
    
    
def test_database_delete_user2(mocked_database_fix, mocked_collection_fix):
    database_object = Database()
    database_object.users_collection = mocked_collection_fix   
    result = database_object.delete_user(user_email = "MockedEmail")
    assert result == {"Info: " f"User with email MockedEmail removed in db"}
    
def test_database_user_update2 (mocked_database_fix, mocked_collection_fix):
    database_object = Database()
    database_object.users_collection = mocked_collection_fix   
    result = database_object.user_update(user = test_user1)
    assert result == {"Info ": f"User with email {test_user1.email}modified in db"}
    
    
def test_database_add_user_error (mocked_database_fix, mocked_collection_fix_error):
    database_object = Database()
    database_object.users_collection = mocked_collection_fix_error 
    user=test_user1
    with pytest.raises(HTTPException)as e_info: 
        database_object.add_user(user)
    assert f"status_code=409, detail='User with email {user.email} not created: duplicated" in str(e_info)    
    
def test_database_add_user_error (mocked_database_fix, mocked_collection_fix):
    database_object = Database()
    database_object.users_collection = mocked_collection_fix
    result = database_object.add_user(test_user1)
    assert result == {"Info ": f"User with email {test_user1.email} added in db"}